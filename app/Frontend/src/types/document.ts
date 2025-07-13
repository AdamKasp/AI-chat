export interface DocumentResponse {
  id: string;
  localisation: string;
  content: string;
  tokens?: number;
  headers?: Record<string, string[]>;
  urls?: string[];
  images?: string[];
  document_metadata?: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface DocumentListResponse {
  documents: DocumentResponse[];
  total: number;
  limit: number;
}

export interface DocumentUploadResponse {
  id: string;
  localisation: string;
  message: string;
  created_at: string;
}

export interface SearchResult {
  id: string;
  content: string;
  file_path: string;
  score: number;
  metadata?: any;
}