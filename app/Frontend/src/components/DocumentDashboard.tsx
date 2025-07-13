import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import DocumentUpload from './DocumentUpload';
import DocumentList from './DocumentList';
import DocumentSearch from './DocumentSearch';
import DocumentViewer from './DocumentViewer';
import { DocumentResponse, SearchResult } from '../types/document';

const DocumentDashboard: React.FC = () => {
  const [selectedDocument, setSelectedDocument] = useState<DocumentResponse | null>(null);
  const [selectedSearchResult, setSelectedSearchResult] = useState<SearchResult | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = () => {
    // Trigger refresh of document list
    setRefreshTrigger(prev => prev + 1);
  };

  const handleDocumentDeleted = () => {
    // Clear selected document if it was deleted and trigger refresh
    setSelectedDocument(null);
    setSelectedSearchResult(null);
    setRefreshTrigger(prev => prev + 1);
  };

  const handleDocumentSelect = (document: DocumentResponse) => {
    setSelectedDocument(document);
    setSelectedSearchResult(null);
  };

  const handleSearchResultSelect = (result: SearchResult) => {
    setSelectedSearchResult(result);
    setSelectedDocument(null);
  };

  const handleCloseViewer = () => {
    setSelectedDocument(null);
    setSelectedSearchResult(null);
  };

  return (
    <Container fluid className="mt-4">
      <Row>
        <Col md={6}>
          <div className="mb-4">
            <DocumentUpload onUploadSuccess={handleUploadSuccess} />
          </div>
          
          <div className="mb-4">
            <DocumentSearch onResultSelect={handleSearchResultSelect} />
          </div>
          
          <div>
            <DocumentList 
              onDocumentSelect={handleDocumentSelect}
              refreshTrigger={refreshTrigger}
              onDocumentDeleted={handleDocumentDeleted}
            />
          </div>
        </Col>
        
        <Col md={6}>
          <DocumentViewer
            document={selectedDocument || undefined}
            searchResult={selectedSearchResult || undefined}
            onClose={handleCloseViewer}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default DocumentDashboard;