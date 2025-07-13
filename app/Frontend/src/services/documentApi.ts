import axios from 'axios';
import { DocumentResponse, DocumentListResponse, DocumentUploadResponse, SearchResult } from '../types/document';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8008';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const documentApi = {
  // POST /documents - Upload a document
  uploadDocument: async (file: File): Promise<DocumentUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<DocumentUploadResponse>('/documents', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // GET /documents - Get list of documents
  getDocuments: async (limit: number = 100, offset: number = 0): Promise<DocumentListResponse> => {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());

    const response = await api.get<DocumentListResponse>(`/documents?${params}`);
    return response.data;
  },

  // GET /documents/search - Search documents
  searchDocuments: async (query: string, limit: number = 10, scoreThreshold?: number): Promise<SearchResult[]> => {
    const params = new URLSearchParams();
    params.append('query', query);
    params.append('limit', limit.toString());
    if (scoreThreshold !== undefined) {
      params.append('score_threshold', scoreThreshold.toString());
    }

    const response = await api.get<SearchResult[]>(`/documents/search?${params}`);
    return response.data;
  },

  // GET /documents/{document_id} - Get specific document
  getDocument: async (documentId: string): Promise<DocumentResponse> => {
    const response = await api.get<DocumentResponse>(`/documents/${documentId}`);
    return response.data;
  },

  // DELETE /documents/{document_id} - Delete specific document
  deleteDocument: async (documentId: string): Promise<{ message: string }> => {
    const response = await api.delete<{ message: string }>(`/documents/${documentId}`);
    return response.data;
  },
};

export default documentApi;