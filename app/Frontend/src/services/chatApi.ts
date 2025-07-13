import axios from 'axios';
import { ChatRequest, ChatResponse, ChatListResponse, AiResponse } from '../types/chat';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8008';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatApi = {
  // POST /chat - Create a new chat or continue existing conversation
  createChat: async (chatRequest: ChatRequest): Promise<AiResponse> => {
    const response = await api.post<AiResponse>('/chat', chatRequest);
    return response.data;
  },

  // POST /chat - Continue existing chat conversation
  continueChat: async (chatId: string, prompt: string, userId: string, model: string = 'gpt-4'): Promise<AiResponse> => {
    const chatRequest: ChatRequest = {
      user_id: userId,
      prompt,
      model,
      chat_id: chatId
    };
    const response = await api.post<AiResponse>('/chat', chatRequest);
    return response.data;
  },

  // GET /chats - Get list of chats
  getChats: async (limit: number = 100, offset: number = 0, userId?: string): Promise<ChatListResponse> => {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());
    if (userId) {
      params.append('user_id', userId);
    }

    const response = await api.get<ChatListResponse>(`/chats?${params}`);
    return response.data;
  },

  // GET /chats/{chat_id} - Get specific chat with full message history
  getChat: async (chatId: string): Promise<ChatResponse> => {
    const response = await api.get<ChatResponse>(`/chats/${chatId}`);
    return response.data;
  },
};

export default chatApi;