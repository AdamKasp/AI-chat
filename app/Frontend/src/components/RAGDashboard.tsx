import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import RAGSearch from './RAGSearch';
import RAGResults from './RAGResults';
import DocumentViewer from './DocumentViewer';
import { RAGSearchResponse } from '../types/rag';
import { DocumentResponse } from '../types/document';

const RAGDashboard: React.FC = () => {
  const [searchResults, setSearchResults] = useState<RAGSearchResponse | null>(null);
  const [selectedDocument, setSelectedDocument] = useState<DocumentResponse | null>(null);

  const handleSearchResult = (results: RAGSearchResponse) => {
    setSearchResults(results);
    setSelectedDocument(null); // Clear selected document when new search is performed
  };

  const handleDocumentSelect = (document: DocumentResponse) => {
    setSelectedDocument(document);
  };

  const handleCloseViewer = () => {
    setSelectedDocument(null);
  };

  return (
    <Container fluid className="mt-4">
      <Row>
        <Col lg={6}>
          <div className="mb-4">
            <RAGSearch onSearchResult={handleSearchResult} />
          </div>
          
          <div>
            <RAGResults 
              results={searchResults}
              onDocumentSelect={handleDocumentSelect}
            />
          </div>
        </Col>
        
        <Col lg={6}>
          <DocumentViewer
            document={selectedDocument || undefined}
            onClose={handleCloseViewer}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default RAGDashboard;