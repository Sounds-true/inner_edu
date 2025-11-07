"""
Link Manager for parent-child linking in InnerWorld Edu.

Manages the linking flow:
1. Child starts bot → provides name
2. Bot generates unique link
3. Child shares link with parent
4. Parent clicks link → activates connection
5. Bot unlocks for child

Security:
- Links expire after 7 days if not activated
- Each child can have only one active parent link
- Parent confirmation required before unlocking bot

Storage:
    src/data/links/{link_id}.json - Link records
    src/data/parents/{parent_id}.json - Parent profiles
"""

import json
import asyncio
import secrets
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

from src.core.logger import get_logger, log_parent_notification

logger = get_logger(__name__)


class LinkStatus(str, Enum):
    """Link status."""
    PENDING = "pending"  # Waiting for parent to activate
    ACTIVE = "active"  # Parent activated, bot unlocked
    EXPIRED = "expired"  # Link expired (7 days)
    REVOKED = "revoked"  # Manually revoked


@dataclass
class ParentLink:
    """Parent-child link record."""
    link_id: str
    child_id: str
    child_name: str
    parent_id: Optional[str] = None
    status: LinkStatus = LinkStatus.PENDING
    created_at: str = ""
    activated_at: Optional[str] = None
    expires_at: str = ""

    def __post_init__(self):
        """Set timestamps if not provided."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

        if not self.expires_at:
            # Links expire after 7 days
            expires = datetime.now() + timedelta(days=7)
            self.expires_at = expires.isoformat()

    def is_expired(self) -> bool:
        """Check if link is expired."""
        if self.status == LinkStatus.EXPIRED:
            return True

        expires = datetime.fromisoformat(self.expires_at)
        return datetime.now() > expires

    def is_active(self) -> bool:
        """Check if link is active."""
        return self.status == LinkStatus.ACTIVE and not self.is_expired()


@dataclass
class ParentProfile:
    """Parent profile."""
    parent_id: str
    children: List[str] = None  # List of child_ids
    notification_settings: Dict[str, bool] = None
    created_at: str = ""
    last_activity: str = ""

    def __post_init__(self):
        """Initialize defaults."""
        if self.children is None:
            self.children = []

        if self.notification_settings is None:
            self.notification_settings = {
                "weekly_reports": True,
                "critical_alerts": True,
                "progress_updates": True,
                "screening_concerns": True
            }

        if not self.created_at:
            self.created_at = datetime.now().isoformat()

        if not self.last_activity:
            self.last_activity = datetime.now().isoformat()


class LinkManager:
    """
    Manages parent-child linking with JSON file storage.

    Creates unique links for parent activation.
    Tracks link status and expiration.
    Manages parent profiles and notifications.
    """

    def __init__(
        self,
        links_dir: Path = Path("src/data/links"),
        parents_dir: Path = Path("src/data/parents")
    ):
        """
        Initialize link manager.

        Args:
            links_dir: Directory for link JSON files
            parents_dir: Directory for parent profile JSON files
        """
        self.links_dir = links_dir
        self.parents_dir = parents_dir

        self.links_dir.mkdir(parents=True, exist_ok=True)
        self.parents_dir.mkdir(parents=True, exist_ok=True)

        logger.info("link_manager_initialized",
                   links_dir=str(links_dir),
                   parents_dir=str(parents_dir))

    def _generate_link_id(self) -> str:
        """Generate unique link ID."""
        return secrets.token_urlsafe(16)

    def _get_link_path(self, link_id: str) -> Path:
        """Get file path for link."""
        return self.links_dir / f"{link_id}.json"

    def _get_parent_path(self, parent_id: str) -> Path:
        """Get file path for parent profile."""
        return self.parents_dir / f"{parent_id}.json"

    async def create_link(
        self,
        child_id: str,
        child_name: str
    ) -> ParentLink:
        """
        Create new parent link for child.

        Args:
            child_id: Child's Telegram ID
            child_name: Child's name

        Returns:
            ParentLink

        Raises:
            ValueError: If child already has active link
        """
        # Check if child already has active link
        existing = await self.get_active_link_by_child(child_id)
        if existing:
            raise ValueError(f"Child {child_id} already has active link")

        # Generate unique link ID
        link_id = self._generate_link_id()

        # Create link
        link = ParentLink(
            link_id=link_id,
            child_id=child_id,
            child_name=child_name
        )

        # Save to disk
        await self._save_link(link)

        logger.info("link_created",
                   link_id=link_id,
                   child_id=child_id,
                   child_name=child_name)

        return link

    async def get_link(self, link_id: str) -> Optional[ParentLink]:
        """
        Get link by ID.

        Args:
            link_id: Link ID

        Returns:
            ParentLink or None
        """
        link_path = self._get_link_path(link_id)

        if not link_path.exists():
            return None

        try:
            async with asyncio.Lock():
                with open(link_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            link = ParentLink(**data)

            # Auto-expire if needed
            if link.status == LinkStatus.PENDING and link.is_expired():
                link.status = LinkStatus.EXPIRED
                await self._save_link(link)

            return link

        except Exception as e:
            logger.error("link_load_failed", link_id=link_id, error=str(e))
            return None

    async def activate_link(
        self,
        link_id: str,
        parent_id: str
    ) -> bool:
        """
        Activate link by parent.

        Args:
            link_id: Link ID
            parent_id: Parent's Telegram ID

        Returns:
            True if successful

        Raises:
            ValueError: If link is invalid, expired, or already activated
        """
        link = await self.get_link(link_id)

        if not link:
            raise ValueError(f"Link {link_id} not found")

        if link.is_expired():
            raise ValueError("Link has expired")

        if link.status == LinkStatus.ACTIVE:
            raise ValueError("Link already activated")

        if link.status == LinkStatus.REVOKED:
            raise ValueError("Link has been revoked")

        # Activate link
        link.parent_id = parent_id
        link.status = LinkStatus.ACTIVE
        link.activated_at = datetime.now().isoformat()

        await self._save_link(link)

        # Update or create parent profile
        parent = await self.get_or_create_parent(parent_id)
        if link.child_id not in parent.children:
            parent.children.append(link.child_id)
            await self._save_parent(parent)

        logger.info("link_activated",
                   link_id=link_id,
                   child_id=link.child_id,
                   parent_id=parent_id)

        log_parent_notification(
            logger,
            event_type="link_activated",
            severity="info",
            user_id=link.child_id,
            parent_id=parent_id
        )

        return True

    async def revoke_link(self, link_id: str) -> bool:
        """
        Revoke link (manual cancellation).

        Args:
            link_id: Link ID

        Returns:
            True if successful
        """
        link = await self.get_link(link_id)

        if not link:
            return False

        link.status = LinkStatus.REVOKED
        await self._save_link(link)

        logger.info("link_revoked", link_id=link_id)
        return True

    async def get_active_link_by_child(self, child_id: str) -> Optional[ParentLink]:
        """
        Get active link for child.

        Args:
            child_id: Child's Telegram ID

        Returns:
            ParentLink or None
        """
        # Search through all links
        for link_path in self.links_dir.glob("*.json"):
            link = await self.get_link(link_path.stem)
            if link and link.child_id == child_id and link.is_active():
                return link

        return None

    async def get_parent(self, parent_id: str) -> Optional[ParentProfile]:
        """
        Get parent profile.

        Args:
            parent_id: Parent's Telegram ID

        Returns:
            ParentProfile or None
        """
        parent_path = self._get_parent_path(parent_id)

        if not parent_path.exists():
            return None

        try:
            async with asyncio.Lock():
                with open(parent_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            return ParentProfile(**data)

        except Exception as e:
            logger.error("parent_load_failed", parent_id=parent_id, error=str(e))
            return None

    async def get_or_create_parent(self, parent_id: str) -> ParentProfile:
        """
        Get existing parent or create new one.

        Args:
            parent_id: Parent's Telegram ID

        Returns:
            ParentProfile
        """
        parent = await self.get_parent(parent_id)

        if not parent:
            parent = ParentProfile(parent_id=parent_id)
            await self._save_parent(parent)
            logger.info("parent_created", parent_id=parent_id)

        return parent

    async def update_parent_settings(
        self,
        parent_id: str,
        notification_settings: Dict[str, bool]
    ) -> bool:
        """
        Update parent notification settings.

        Args:
            parent_id: Parent's Telegram ID
            notification_settings: Settings dict

        Returns:
            True if successful
        """
        parent = await self.get_or_create_parent(parent_id)
        parent.notification_settings.update(notification_settings)
        parent.last_activity = datetime.now().isoformat()

        await self._save_parent(parent)

        logger.info("parent_settings_updated", parent_id=parent_id)
        return True

    async def get_parent_children(self, parent_id: str) -> List[str]:
        """
        Get list of children for parent.

        Args:
            parent_id: Parent's Telegram ID

        Returns:
            List of child IDs
        """
        parent = await self.get_parent(parent_id)

        if not parent:
            return []

        return parent.children

    async def is_child_linked(self, child_id: str) -> bool:
        """
        Check if child has active parent link.

        Args:
            child_id: Child's Telegram ID

        Returns:
            True if linked
        """
        link = await self.get_active_link_by_child(child_id)
        return link is not None

    async def get_parent_for_child(self, child_id: str) -> Optional[str]:
        """
        Get parent ID for child.

        Args:
            child_id: Child's Telegram ID

        Returns:
            Parent ID or None
        """
        link = await self.get_active_link_by_child(child_id)

        if link and link.is_active():
            return link.parent_id

        return None

    def generate_link_url(self, link_id: str, bot_username: str = "innerworld_edu_parent_bot") -> str:
        """
        Generate deep link URL for Telegram.

        Args:
            link_id: Link ID
            bot_username: Parent bot username

        Returns:
            Deep link URL
        """
        return f"https://t.me/{bot_username}?start=link_{link_id}"

    async def _save_link(self, link: ParentLink) -> None:
        """Save link to disk."""
        link_path = self._get_link_path(link.link_id)
        data = asdict(link)

        async with asyncio.Lock():
            temp_path = link_path.with_suffix('.tmp')

            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            temp_path.replace(link_path)

    async def _save_parent(self, parent: ParentProfile) -> None:
        """Save parent profile to disk."""
        parent_path = self._get_parent_path(parent.parent_id)
        data = asdict(parent)

        async with asyncio.Lock():
            temp_path = parent_path.with_suffix('.tmp')

            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            temp_path.replace(parent_path)

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get linking statistics.

        Returns:
            Dictionary with statistics
        """
        total_links = 0
        active_links = 0
        pending_links = 0
        expired_links = 0

        for link_path in self.links_dir.glob("*.json"):
            link = await self.get_link(link_path.stem)
            if link:
                total_links += 1

                if link.status == LinkStatus.ACTIVE:
                    active_links += 1
                elif link.status == LinkStatus.PENDING:
                    if link.is_expired():
                        expired_links += 1
                    else:
                        pending_links += 1
                elif link.status == LinkStatus.EXPIRED:
                    expired_links += 1

        total_parents = len(list(self.parents_dir.glob("*.json")))

        return {
            "total_links": total_links,
            "active_links": active_links,
            "pending_links": pending_links,
            "expired_links": expired_links,
            "total_parents": total_parents,
            "avg_children_per_parent": active_links / total_parents if total_parents > 0 else 0
        }
