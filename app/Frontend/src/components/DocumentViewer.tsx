import React, { useState, useEffect } from 'react';
import { Card, Button, Spinner, Alert, Badge } from 'react-bootstrap';
import { documentApi } from '../services/documentApi';
import { DocumentResponse, SearchResult } from '../types/document';

interface DocumentViewerProps {
  document?: DocumentResponse;
  searchResult?: SearchResult;
  documentId?: string;
  onClose?: () => void;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ 
  document, 
  searchResult, 
  documentId, 
  onClose 
}) => {
  const [currentDocument, setCurrentDocument] = useState<DocumentResponse | null>(document || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (documentId && !document && !searchResult) {
      loadDocument(documentId);
    } else if (searchResult) {
      loadDocument(searchResult.id);
    } else if (document) {
      setCurrentDocument(document);
    }
  }, [documentId, document, searchResult]);

  const loadDocument = async (id: string) => {
    setLoading(true);
    setError(null);

    try {
      const doc = await documentApi.getDocument(id);
      setCurrentDocument(doc);
    } catch (err) {
      setError('Failed to load document');
      console.error('Error loading document:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Card>
        <Card.Body className="text-center">
          <Spinner animation="border" />
          <div className="mt-2">Loading document...</div>
        </Card.Body>
      </Card>
    );
  }

  if (error) {
    return (
      <Alert variant="danger">
        {error}
        {onClose && (
          <div className="mt-2">
            <Button variant="outline-danger" size="sm" onClick={onClose}>
              Close
            </Button>
          </div>
        )}
      </Alert>
    );
  }

  if (!currentDocument) {
    return (
      <Card>
        <Card.Body className="text-center text-muted">
          No document selected
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card>
      <Card.Header className="d-flex justify-content-between align-items-center">
        <div>
          <h5 className="mb-0">{currentDocument.localisation}</h5>
          {searchResult && (
            <Badge bg="info" className="mt-1">
              Match: {(searchResult.score * 100).toFixed(1)}%
            </Badge>
          )}
        </div>
        {onClose && (
          <Button variant="outline-secondary" size="sm" onClick={onClose}>
            ✕
          </Button>
        )}
      </Card.Header>
      <Card.Body>
        <div className="mb-3">
          <small className="text-muted">
            Created: {new Date(currentDocument.created_at).toLocaleString()}
            {currentDocument.updated_at && (
              <> | Updated: {new Date(currentDocument.updated_at).toLocaleString()}</>
            )}
          </small>
        </div>
        
        <div 
          style={{ 
            maxHeight: '400px', 
            overflowY: 'auto',
            whiteSpace: 'pre-wrap',
            lineHeight: '1.6',
            fontSize: '14px'
          }}
          className="border rounded p-3 bg-light"
        >
          {currentDocument.content}
        </div>
        
        <div className="mt-3">
          <small className="text-muted">
            Document ID: {currentDocument.id} | 
            {currentDocument.tokens ? `Tokens: ${currentDocument.tokens}` : `Content length: ${currentDocument.content.length} characters`}
          </small>
        </div>
      </Card.Body>
    </Card>
  );
};

export default DocumentViewer;