"""
Reality Bridge Manager - Manages micro-action reminders.

Handles scheduling, tracking, and reminders for Reality Bridge actions.
Uses APScheduler for reminder delivery and JSON for persistence.
"""

import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, Callable, Awaitable, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from src.core.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ActiveBridge:
    """Active Reality Bridge tracking."""
    user_id: str
    quest_id: str
    bridge_id: str
    title: str
    description: str

    # Timing
    created_at: str  # ISO timestamp
    deadline_at: str  # ISO timestamp
    reminder_at: str  # ISO timestamp

    # Status
    completed: bool = False
    reminded: bool = False
    verification_response: Optional[str] = None
    completed_at: Optional[str] = None


class RealityBridgeManager:
    """Manages Reality Bridge micro-actions and reminders."""

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize Reality Bridge Manager.

        Args:
            storage_path: Path to store active bridges (default: src/data/reality_bridges/)
        """
        self.storage_path = storage_path or Path("src/data/reality_bridges")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Active bridges by user_id
        self.active_bridges: Dict[str, ActiveBridge] = {}

        # Scheduler for reminders
        self.scheduler = AsyncIOScheduler()

        # Callback for sending reminders (will be set by StateManager/Bot)
        self.reminder_callback: Optional[Callable[[str, ActiveBridge], Awaitable[None]]] = None

        self.initialized = False

    async def initialize(self) -> None:
        """Initialize scheduler and load active bridges."""
        try:
            # Load active bridges from storage
            await self._load_active_bridges()

            # Start scheduler
            self.scheduler.start()
            logger.info("reality_bridge_manager_initialized",
                       active_bridges=len(self.active_bridges))

            # Reschedule existing reminders
            await self._reschedule_reminders()

            self.initialized = True

        except Exception as e:
            logger.error("reality_bridge_manager_init_failed", error=str(e))
            raise

    async def shutdown(self) -> None:
        """Shutdown scheduler gracefully."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("reality_bridge_manager_shutdown")

    def set_reminder_callback(
        self,
        callback: Callable[[str, ActiveBridge], Awaitable[None]]
    ) -> None:
        """
        Set callback for sending reminders.

        Args:
            callback: Async function(user_id, bridge) to send reminder
        """
        self.reminder_callback = callback
        logger.info("reminder_callback_set")

    async def create_bridge(
        self,
        user_id: str,
        quest_id: str,
        bridge_id: str,
        title: str,
        description: str,
        deadline_hours: int = 48,
        reminder_hours: int = 24
    ) -> ActiveBridge:
        """
        Create new Reality Bridge for user.

        Args:
            user_id: User ID
            quest_id: Quest ID that generated this bridge
            bridge_id: Bridge ID
            title: Bridge title
            description: Bridge description
            deadline_hours: Hours until deadline
            reminder_hours: Hours until reminder

        Returns:
            ActiveBridge
        """
        now = datetime.now()
        deadline = now + timedelta(hours=deadline_hours)
        reminder = now + timedelta(hours=reminder_hours)

        # Create active bridge
        bridge = ActiveBridge(
            user_id=user_id,
            quest_id=quest_id,
            bridge_id=bridge_id,
            title=title,
            description=description,
            created_at=now.isoformat(),
            deadline_at=deadline.isoformat(),
            reminder_at=reminder.isoformat()
        )

        # Store in memory and disk
        self.active_bridges[user_id] = bridge
        await self._save_bridge(bridge)

        # Schedule reminder
        await self._schedule_reminder(bridge)

        logger.info("reality_bridge_created",
                   user_id=user_id,
                   bridge_id=bridge_id,
                   reminder_at=reminder.isoformat(),
                   deadline_at=deadline.isoformat())

        return bridge

    async def complete_bridge(
        self,
        user_id: str,
        verification_response: Optional[str] = None
    ) -> bool:
        """
        Mark Reality Bridge as completed.

        Args:
            user_id: User ID
            verification_response: User's response to verification

        Returns:
            True if successful
        """
        bridge = self.active_bridges.get(user_id)

        if not bridge:
            logger.warning("complete_bridge_not_found", user_id=user_id)
            return False

        # Mark as completed
        bridge.completed = True
        bridge.verification_response = verification_response
        bridge.completed_at = datetime.now().isoformat()

        # Save to disk
        await self._save_bridge(bridge)

        # Cancel reminder if not sent yet
        if not bridge.reminded:
            self._cancel_reminder(user_id)

        logger.info("reality_bridge_completed",
                   user_id=user_id,
                   bridge_id=bridge.bridge_id)

        return True

    async def get_active_bridge(self, user_id: str) -> Optional[ActiveBridge]:
        """Get active Reality Bridge for user."""
        return self.active_bridges.get(user_id)

    async def check_deadlines(self) -> List[ActiveBridge]:
        """
        Check for expired Reality Bridges.

        Returns:
            List of expired bridges
        """
        now = datetime.now()
        expired = []

        for bridge in self.active_bridges.values():
            if bridge.completed:
                continue

            deadline = datetime.fromisoformat(bridge.deadline_at)
            if now > deadline:
                expired.append(bridge)
                logger.warning("reality_bridge_expired",
                             user_id=bridge.user_id,
                             bridge_id=bridge.bridge_id)

        return expired

    async def _schedule_reminder(self, bridge: ActiveBridge) -> None:
        """Schedule reminder for bridge."""
        if not self.reminder_callback:
            logger.warning("reminder_callback_not_set", user_id=bridge.user_id)
            return

        reminder_time = datetime.fromisoformat(bridge.reminder_at)

        # Don't schedule if reminder time has passed
        if datetime.now() >= reminder_time:
            logger.warning("reminder_time_passed",
                         user_id=bridge.user_id,
                         reminder_at=bridge.reminder_at)
            return

        # Schedule job
        self.scheduler.add_job(
            self._send_reminder,
            trigger=DateTrigger(run_date=reminder_time),
            args=[bridge.user_id],
            id=f"reminder_{bridge.user_id}",
            replace_existing=True
        )

        logger.info("reminder_scheduled",
                   user_id=bridge.user_id,
                   reminder_at=reminder_time.isoformat())

    def _cancel_reminder(self, user_id: str) -> None:
        """Cancel scheduled reminder."""
        job_id = f"reminder_{user_id}"

        try:
            self.scheduler.remove_job(job_id)
            logger.info("reminder_cancelled", user_id=user_id)
        except Exception as e:
            logger.debug("reminder_cancel_failed", user_id=user_id, error=str(e))

    async def _send_reminder(self, user_id: str) -> None:
        """Send reminder to user."""
        bridge = self.active_bridges.get(user_id)

        if not bridge:
            logger.warning("send_reminder_bridge_not_found", user_id=user_id)
            return

        if bridge.completed:
            logger.info("send_reminder_already_completed", user_id=user_id)
            return

        # Mark as reminded
        bridge.reminded = True
        await self._save_bridge(bridge)

        # Call callback
        if self.reminder_callback:
            try:
                await self.reminder_callback(user_id, bridge)
                logger.info("reminder_sent",
                           user_id=user_id,
                           bridge_id=bridge.bridge_id)
            except Exception as e:
                logger.error("reminder_callback_failed",
                           user_id=user_id,
                           error=str(e))
        else:
            logger.warning("reminder_callback_not_set", user_id=user_id)

    async def _reschedule_reminders(self) -> None:
        """Reschedule reminders after restart."""
        for bridge in self.active_bridges.values():
            if not bridge.completed and not bridge.reminded:
                await self._schedule_reminder(bridge)

    async def _load_active_bridges(self) -> None:
        """Load active bridges from storage."""
        for bridge_file in self.storage_path.glob("*.json"):
            try:
                with open(bridge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                bridge = ActiveBridge(**data)

                # Only load if not completed and not expired
                deadline = datetime.fromisoformat(bridge.deadline_at)
                if not bridge.completed and datetime.now() < deadline:
                    self.active_bridges[bridge.user_id] = bridge
                    logger.debug("bridge_loaded", user_id=bridge.user_id)

            except Exception as e:
                logger.error("bridge_load_failed",
                           file=bridge_file.name,
                           error=str(e))

    async def _save_bridge(self, bridge: ActiveBridge) -> None:
        """Save bridge to storage."""
        bridge_path = self.storage_path / f"{bridge.user_id}.json"

        try:
            async with asyncio.Lock():
                with open(bridge_path, 'w', encoding='utf-8') as f:
                    json.dump(asdict(bridge), f, indent=2, ensure_ascii=False)

            logger.debug("bridge_saved", user_id=bridge.user_id)

        except Exception as e:
            logger.error("bridge_save_failed",
                        user_id=bridge.user_id,
                        error=str(e))

    def _get_bridge_path(self, user_id: str) -> Path:
        """Get storage path for user's bridge."""
        return self.storage_path / f"{user_id}.json"
