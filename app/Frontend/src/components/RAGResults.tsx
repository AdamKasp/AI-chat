import React, { useState } from 'react';
import { Card, Badge, ListGroup, Collapse, Button, Alert, Row, Col } from 'react-bootstrap';
import { RAGSearchResponse } from '../types/rag';
import { DocumentResponse } from '../types/document';

interface RAGResultsProps {
  results: RAGSearchResponse | null;
  onDocumentSelect?: (document: DocumentResponse) => void;
}

const RAGResults: React.FC<RAGResultsProps> = ({ results, onDocumentSelect }) => {
  const [showContext, setShowContext] = useState(false);
  const [showMetadata, setShowMetadata] = useState(false);

  if (!results) {
    return (
      <Card>
        <Card.Body className="text-center text-muted">
          <div className="py-4">
            🔍 Enter a search query to see RAG results
          </div>
        </Card.Body>
      </Card>
    );
  }

  if (results.error) {
    return (
      <Card>
        <Card.Body>
          <Alert variant="danger">
            <Alert.Heading>Search Error</Alert.Heading>
            {results.error}
          </Alert>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card>
      <Card.Header className="d-flex justify-content-between align-items-center">
        <div>
          <h5 className="mb-0">🎯 RAG Search Results</h5>
          <small className="text-muted">Query: "{results.query}"</small>
        </div>
        <div className="d-flex gap-2">
          <Badge bg="primary">{results.document_count} docs</Badge>
          <Badge bg="info">{results.context_length} chars</Badge>
        </div>
      </Card.Header>

      <Card.Body>
        {results.document_count === 0 ? (
          <Alert variant="warning">
            <Alert.Heading>No Documents Found</Alert.Heading>
            No documents matched your search query. Try using different keywords or reducing the score threshold.
          </Alert>
        ) : (
          <>
            {/* Metadata Summary */}
            <Row className="mb-3">
              <Col>
                <Button
                  variant="outline-info"
                  size="sm"
                  onClick={() => setShowMetadata(!showMetadata)}
                  className="me-2"
                >
                  📊 {showMetadata ? 'Hide' : 'Show'} Metadata
                </Button>
                <Button
                  variant="outline-secondary"
                  size="sm"
                  onClick={() => setShowContext(!showContext)}
                >
                  📄 {showContext ? 'Hide' : 'Show'} Context
                </Button>
              </Col>
            </Row>

            {/* Metadata Details */}
            <Collapse in={showMetadata}>
              <div className="mb-3">
                <Card bg="light">
                  <Card.Body>
                    <Row>
                      <Col md={3}>
                        <strong>Documents Found:</strong><br />
                        <Badge bg="success">{results.document_count}</Badge>
                      </Col>
                      <Col md={3}>
                        <strong>Context Length:</strong><br />
                        <Badge bg="info">{results.context_length} characters</Badge>
                      </Col>
                      <Col md={3}>
                        <strong>Has Context:</strong><br />
                        <Badge bg={results.has_context ? "success" : "warning"}>
                          {results.has_context ? "Yes" : "No"}
                        </Badge>
                      </Col>
                      <Col md={3}>
                        <strong>Sources:</strong><br />
                        <small>{results.document_sources.length} files</small>
                      </Col>
                    </Row>
                    <Row className="mt-2">
                      <Col>
                        <strong>Source Files:</strong><br />
                        <div className="d-flex flex-wrap gap-1 mt-1">
                          {results.document_sources.map((source, index) => (
                            <Badge key={index} bg="secondary" className="text-wrap">
                              {source}
                            </Badge>
                          ))}
                        </div>
                      </Col>
                    </Row>
                  </Card.Body>
                </Card>
              </div>
            </Collapse>

            {/* Context Display */}
            <Collapse in={showContext}>
              <div className="mb-3">
                <Card>
                  <Card.Header>
                    <h6 className="mb-0">📄 Formatted Context</h6>
                  </Card.Header>
                  <Card.Body>
                    <pre style={{ 
                      whiteSpace: 'pre-wrap', 
                      fontSize: '0.9em',
                      maxHeight: '300px',
                      overflowY: 'auto'
                    }}>
                      {results.context || 'No context available'}
                    </pre>
                  </Card.Body>
                </Card>
              </div>
            </Collapse>

            {/* Documents List */}
            <div>
              <h6 className="mb-2">📚 Retrieved Documents</h6>
              <ListGroup variant="flush">
                {results.documents.map((document, index) => (
                  <ListGroup.Item 
                    key={document.id}
                    action={!!onDocumentSelect}
                    onClick={() => onDocumentSelect?.(document)}
                    className="d-flex justify-content-between align-items-start"
                  >
                    <div className="flex-grow-1">
                      <div className="d-flex justify-content-between align-items-start mb-1">
                        <strong className="text-primary">
                          {index + 1}. {document.localisation}
                        </strong>
                        <Badge bg="secondary" className="ms-2">
                          {document.tokens ? `${document.tokens} tokens` : `${document.content.length} chars`}
                        </Badge>
                      </div>
                      <div className="text-muted small mb-2">
                        {document.content.substring(0, 150)}
                        {document.content.length > 150 && '...'}
                      </div>
                      <div className="text-muted small">
                        Created: {new Date(document.created_at).toLocaleDateString()}
                        {document.headers && Object.keys(document.headers).length > 0 && (
                          <span className="ms-2">
                            • Headers: {Object.keys(document.headers).join(', ')}
                          </span>
                        )}
                      </div>
                    </div>
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </div>
          </>
        )}
      </Card.Body>
    </Card>
  );
};

export default RAGResults;