export interface ChatRequest {
  user_id: string;
  prompt: string;
  model: string;
  chat_id?: string;
  system_prompt?: string;
}

export interface Message {
  id: string;
  message: string;
  author: 'user' | 'agent';
  created_at: string;
}

export interface ChatResponse {
  id: string;
  user_id: string;
  created_at: string;
  updated_at?: string;
  messages: Message[];
  // Backward compatibility helpers
  last_user_message?: string;
  last_agent_response?: string;
}

export interface ChatListResponse {
  chats: ChatResponse[];
  total: number;
  limit: number;
  offset?: number;
}

export interface AiResponse {
  finishReason: string;
  answer: string;
  metadata: {
    usage?: any;
    chat_id: string;
    rag_info?: any;
  };
}