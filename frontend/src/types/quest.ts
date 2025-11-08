/**
 * TypeScript типы для квестов и графов
 */

export type NodeType = 'start' | 'questStep' | 'choice' | 'realityBridge' | 'end';

export interface QuestNode {
  id: string;
  type: NodeType;
  position: {
    x: number;
    y: number;
  };
  data: Record<string, any>;
}

export interface QuestEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  animated?: boolean;
}

export interface QuestGraph {
  nodes: QuestNode[];
  edges: QuestEdge[];
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface QuestContext {
  age?: number;
  topic?: string;
  difficulties?: string[];
  num_steps?: number;
  preferences?: string;
}

export interface BuilderSession {
  session_id: string;
  user_id: string;
  conversation_history: ChatMessage[];
  current_stage: string;
  current_graph: QuestGraph | null;
  quest_context: QuestContext;
}
