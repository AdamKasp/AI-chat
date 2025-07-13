import axios from 'axios';
import { RAGSearchResponse } from '../types/rag';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8008';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ragApi = {
  // GET /rag/search - Search documents using RAG
  searchDocuments: async (
    prompt: string, 
    count: number = 5, 
    scoreThreshold?: number
  ): Promise<RAGSearchResponse> => {
    const params = new URLSearchParams();
    params.append('prompt', prompt);
    params.append('count', count.toString());
    if (scoreThreshold !== undefined) {
      params.append('score_threshold', scoreThreshold.toString());
    }

    const response = await api.get<RAGSearchResponse>(`/rag/search?${params}`);
    return response.data;
  },
};

export default ragApi;