-- Migration to add metadata columns to documents table
-- Run this script to update your existing database schema

ALTER TABLE documents ADD COLUMN IF NOT EXISTS tokens INTEGER;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS headers JSON;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS urls JSON;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS images JSON;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS document_metadata JSON;

-- Add comments to document the purpose of each column
COMMENT ON COLUMN documents.tokens IS 'Number of tokens in the document';
COMMENT ON COLUMN documents.headers IS 'Extracted headers from the document (h1-h6)';
COMMENT ON COLUMN documents.urls IS 'List of URLs found in the document';
COMMENT ON COLUMN documents.images IS 'List of images found in the document';
COMMENT ON COLUMN documents.document_metadata IS 'Additional metadata for the document';