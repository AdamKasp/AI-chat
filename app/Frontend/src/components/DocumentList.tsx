import React, { useState, useEffect } from 'react';
import { Card, ListGroup, Badge, Spinner, Alert, Button, Modal } from 'react-bootstrap';
import { documentApi } from '../services/documentApi';
import { DocumentResponse } from '../types/document';

interface DocumentListProps {
  onDocumentSelect?: (document: DocumentResponse) => void;
  refreshTrigger?: number;
  onDocumentDeleted?: () => void;
}

const DocumentList: React.FC<DocumentListProps> = ({ onDocumentSelect, refreshTrigger, onDocumentDeleted }) => {
  const [documents, setDocuments] = useState<DocumentResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [deleteLoading, setDeleteLoading] = useState<string | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [documentToDelete, setDocumentToDelete] = useState<DocumentResponse | null>(null);

  const loadDocuments = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await documentApi.getDocuments();
      setDocuments(response.documents);
    } catch (err) {
      setError('Failed to load documents');
      console.error('Error loading documents:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, [refreshTrigger]);

  const handleDeleteClick = (document: DocumentResponse, event: React.MouseEvent) => {
    event.stopPropagation();
    setDocumentToDelete(document);
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = async () => {
    if (!documentToDelete) return;

    setDeleteLoading(documentToDelete.id);
    setError(null);

    try {
      await documentApi.deleteDocument(documentToDelete.id);
      setDocuments(docs => docs.filter(doc => doc.id !== documentToDelete.id));
      setShowDeleteModal(false);
      setDocumentToDelete(null);
      onDocumentDeleted?.();
    } catch (err) {
      setError('Failed to delete document');
      console.error('Error deleting document:', err);
    } finally {
      setDeleteLoading(null);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
    setDocumentToDelete(null);
  };

  if (loading) {
    return (
      <Card>
        <Card.Body className="text-center">
          <Spinner animation="border" />
          <div className="mt-2">Loading documents...</div>
        </Card.Body>
      </Card>
    );
  }

  if (error) {
    return (
      <Alert variant="danger">
        {error}
      </Alert>
    );
  }

  return (
    <Card>
      <Card.Header>
        <h5 className="mb-0">Documents ({documents.length})</h5>
      </Card.Header>
      <Card.Body style={{ maxHeight: '400px', overflowY: 'auto' }}>
        {documents.length === 0 ? (
          <div className="text-muted text-center">No documents found</div>
        ) : (
          <ListGroup variant="flush">
            {documents.map((document) => (
              <ListGroup.Item 
                key={document.id}
                action={!!onDocumentSelect}
                onClick={() => onDocumentSelect?.(document)}
                className="d-flex justify-content-between align-items-start"
              >
                <div className="flex-grow-1">
                  <div className="fw-bold">{document.localisation}</div>
                  <div className="text-muted small">
                    {document.content.substring(0, 100)}
                    {document.content.length > 100 && '...'}
                  </div>
                  <div className="text-muted small">
                    Created: {new Date(document.created_at).toLocaleDateString()}
                  </div>
                </div>
                <div className="d-flex align-items-center gap-2">
                  <Badge bg="secondary">
                    {document.tokens ? `${document.tokens} tokens` : `${document.content.length} chars`}
                  </Badge>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={(e) => handleDeleteClick(document, e)}
                    disabled={deleteLoading === document.id}
                  >
                    {deleteLoading === document.id ? (
                      <Spinner animation="border" size="sm" />
                    ) : (
                      '🗑️'
                    )}
                  </Button>
                </div>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Card.Body>

      {/* Delete Confirmation Modal */}
      <Modal show={showDeleteModal} onHide={handleDeleteCancel} centered>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Document Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Are you sure you want to delete this document?</p>
          {documentToDelete && (
            <div className="bg-light p-3 rounded">
              <strong>{documentToDelete.localisation}</strong>
              <div className="text-muted small mt-1">
                {documentToDelete.content.substring(0, 100)}
                {documentToDelete.content.length > 100 && '...'}
              </div>
            </div>
          )}
          <p className="text-warning mt-3 mb-0">
            <small>⚠️ This action cannot be undone. The document will be permanently deleted from both the database and vector search index.</small>
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleDeleteCancel}>
            Cancel
          </Button>
          <Button 
            variant="danger" 
            onClick={handleDeleteConfirm}
            disabled={deleteLoading !== null}
          >
            {deleteLoading ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                Deleting...
              </>
            ) : (
              'Delete Document'
            )}
          </Button>
        </Modal.Footer>
      </Modal>
    </Card>
  );
};

export default DocumentList;