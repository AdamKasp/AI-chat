import React, { useState } from 'react';
import { Card, Form, Button, ListGroup, Badge, Spinner, Alert, InputGroup } from 'react-bootstrap';
import { documentApi } from '../services/documentApi';
import { SearchResult } from '../types/document';

interface DocumentSearchProps {
  onResultSelect?: (result: SearchResult) => void;
}

const DocumentSearch: React.FC<DocumentSearchProps> = ({ onResultSelect }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setSearching(true);
    setError(null);

    try {
      const searchResults = await documentApi.searchDocuments(query.trim());
      setResults(searchResults);
    } catch (err) {
      setError('Failed to search documents');
      console.error('Search error:', err);
    } finally {
      setSearching(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'secondary';
  };

  return (
    <Card>
      <Card.Header>
        <h5 className="mb-0">Search Documents</h5>
      </Card.Header>
      <Card.Body>
        <Form>
          <InputGroup className="mb-3">
            <Form.Control
              type="text"
              placeholder="Enter search query..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={searching}
            />
            <Button
              variant="outline-primary"
              onClick={handleSearch}
              disabled={searching || !query.trim()}
            >
              {searching ? <Spinner size="sm" /> : 'Search'}
            </Button>
          </InputGroup>

          {error && (
            <Alert variant="danger" className="mb-3">
              {error}
            </Alert>
          )}

          {results.length > 0 && (
            <div>
              <h6>Search Results ({results.length})</h6>
              <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                <ListGroup variant="flush">
                  {results.map((result, index) => (
                    <ListGroup.Item
                      key={index}
                      action={!!onResultSelect}
                      onClick={() => onResultSelect?.(result)}
                      className="d-flex justify-content-between align-items-start"
                    >
                      <div className="flex-grow-1">
                        <div className="fw-bold">{result.file_path}</div>
                        <div className="text-muted small mb-1">
                          {result.content.substring(0, 150)}
                          {result.content.length > 150 && '...'}
                        </div>
                        <div className="text-muted small">
                          Document ID: {result.id}
                        </div>
                      </div>
                      <Badge bg={getScoreColor(result.score)} className="ms-2">
                        {(result.score * 100).toFixed(1)}%
                      </Badge>
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              </div>
            </div>
          )}

          {results.length === 0 && query && !searching && !error && (
            <div className="text-muted text-center mt-3">
              No results found for "{query}"
            </div>
          )}
        </Form>
      </Card.Body>
    </Card>
  );
};

export default DocumentSearch;