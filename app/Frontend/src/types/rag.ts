import { DocumentResponse } from './document';

export interface RAGSearchResponse {
  query: string;
  document_count: number;
  documents: DocumentResponse[];
  context: string;
  context_length: number;
  has_context: boolean;
  document_sources: string[];
  error: string | null;
}

export interface RAGSearchRequest {
  prompt: string;
  count?: number;
  score_threshold?: number;
}

export interface RAGSearchResult {
  query: string;
  documents: DocumentResponse[];
  context: string;
  metadata: {
    document_count: number;
    context_length: number;
    has_context: boolean;
    document_sources: string[];
    search_time?: number;
  };
  error?: string;
}