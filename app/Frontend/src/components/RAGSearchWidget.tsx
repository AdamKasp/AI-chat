import React, { useState } from 'react';
import { Card, Form, Button, Spinner, Badge, Collapse } from 'react-bootstrap';
import { ragApi } from '../services/ragApi';
import { RAGSearchResponse } from '../types/rag';
import { DocumentResponse } from '../types/document';

interface RAGSearchWidgetProps {
  onDocumentSelect?: (document: DocumentResponse) => void;
}

const RAGSearchWidget: React.FC<RAGSearchWidgetProps> = ({ onDocumentSelect }) => {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<RAGSearchResponse | null>(null);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prompt.trim()) return;

    setLoading(true);
    try {
      const searchResults = await ragApi.searchDocuments(prompt.trim(), 5);
      setResults(searchResults);
      setShowResults(true);
    } catch (err) {
      console.error('RAG search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <Card.Header>
        <h6 className="mb-0">🧠 Smart Document Search (RAG)</h6>
      </Card.Header>
      <Card.Body>
        <Form onSubmit={handleSearch}>
          <div className="d-flex gap-2 mb-3">
            <Form.Control
              type="text"
              placeholder="Ask about your documents..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={loading}
              size="sm"
            />
            <Button
              type="submit"
              variant="primary"
              size="sm"
              disabled={loading || !prompt.trim()}
            >
              {loading ? <Spinner animation="border" size="sm" /> : '🔍'}
            </Button>
          </div>
        </Form>

        {results && (
          <>
            <div className="d-flex justify-content-between align-items-center mb-2">
              <div className="d-flex gap-2">
                <Badge bg="info">{results.document_count} docs</Badge>
                <Badge bg="secondary">{results.context_length} chars</Badge>
              </div>
              <Button
                variant="outline-secondary"
                size="sm"
                onClick={() => setShowResults(!showResults)}
              >
                {showResults ? 'Hide' : 'Show'} Results
              </Button>
            </div>

            <Collapse in={showResults}>
              <div>
                {results.documents.length > 0 ? (
                  <div className="list-group list-group-flush">
                    {results.documents.slice(0, 3).map((doc, index) => (
                      <div
                        key={doc.id}
                        className="list-group-item list-group-item-action p-2"
                        style={{ cursor: 'pointer' }}
                        onClick={() => onDocumentSelect?.(doc)}
                      >
                        <div className="d-flex justify-content-between align-items-start">
                          <div className="flex-grow-1">
                            <div className="fw-bold small text-primary">
                              {index + 1}. {doc.localisation}
                            </div>
                            <div className="text-muted small">
                              {doc.content.substring(0, 80)}...
                            </div>
                          </div>
                          <Badge bg="light" text="dark" className="ms-2">
                            {doc.tokens || Math.round(doc.content.length / 4)}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <small className="text-muted">No documents found for this query.</small>
                )}
              </div>
            </Collapse>
          </>
        )}
      </Card.Body>
    </Card>
  );
};

export default RAGSearchWidget;