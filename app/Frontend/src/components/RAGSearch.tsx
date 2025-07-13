import React, { useState } from 'react';
import { Card, Form, Button, Spinner, Alert, InputGroup, Row, Col } from 'react-bootstrap';
import { ragApi } from '../services/ragApi';
import { RAGSearchResponse } from '../types/rag';

interface RAGSearchProps {
  onSearchResult?: (result: RAGSearchResponse) => void;
}

const RAGSearch: React.FC<RAGSearchProps> = ({ onSearchResult }) => {
  const [prompt, setPrompt] = useState('');
  const [count, setCount] = useState(5);
  const [scoreThreshold, setScoreThreshold] = useState<number | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Please enter a search prompt');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await ragApi.searchDocuments(prompt.trim(), count, scoreThreshold);
      onSearchResult?.(result);
      
      if (result.error) {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to search documents');
      console.error('RAG search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPrompt('');
    setCount(5);
    setScoreThreshold(undefined);
    setError(null);
  };

  return (
    <Card>
      <Card.Header>
        <h5 className="mb-0">🔍 RAG Document Search</h5>
        <small className="text-muted">
          Retrieve documents using semantic similarity search
        </small>
      </Card.Header>
      <Card.Body>
        <Form onSubmit={handleSearch}>
          <Form.Group className="mb-3">
            <Form.Label>Search Prompt</Form.Label>
            <InputGroup>
              <Form.Control
                type="text"
                placeholder="Enter your search query (e.g., 'programming tools', 'version control')"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                disabled={loading}
              />
              <Button
                variant="outline-secondary"
                onClick={handleReset}
                disabled={loading}
                title="Clear search"
              >
                ✕
              </Button>
            </InputGroup>
          </Form.Group>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Number of Documents</Form.Label>
                <Form.Select
                  value={count}
                  onChange={(e) => setCount(parseInt(e.target.value))}
                  disabled={loading}
                >
                  <option value={1}>1 document</option>
                  <option value={3}>3 documents</option>
                  <option value={5}>5 documents</option>
                  <option value={10}>10 documents</option>
                  <option value={20}>20 documents</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Score Threshold (Optional)</Form.Label>
                <Form.Control
                  type="number"
                  placeholder="0.0 - 1.0"
                  step="0.1"
                  min="0"
                  max="1"
                  value={scoreThreshold || ''}
                  onChange={(e) => 
                    setScoreThreshold(e.target.value ? parseFloat(e.target.value) : undefined)
                  }
                  disabled={loading}
                />
                <Form.Text className="text-muted">
                  Minimum similarity score (higher = more strict)
                </Form.Text>
              </Form.Group>
            </Col>
          </Row>

          {error && (
            <Alert variant="danger" className="mb-3">
              {error}
            </Alert>
          )}

          <div className="d-grid">
            <Button
              type="submit"
              variant="primary"
              disabled={loading || !prompt.trim()}
            >
              {loading ? (
                <>
                  <Spinner animation="border" size="sm" className="me-2" />
                  Searching...
                </>
              ) : (
                '🔍 Search Documents'
              )}
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default RAGSearch;