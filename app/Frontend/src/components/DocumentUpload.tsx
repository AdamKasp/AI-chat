import React, { useState } from 'react';
import { Card, Form, Button, Alert, ProgressBar } from 'react-bootstrap';
import { documentApi } from '../services/documentApi';

interface DocumentUploadProps {
  onUploadSuccess?: () => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
    setMessage(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage({ type: 'error', text: 'Please select a file to upload' });
      return;
    }

    setUploading(true);
    setUploadProgress(0);
    setMessage(null);

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 100);

      const response = await documentApi.uploadDocument(selectedFile);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      setMessage({ type: 'success', text: response.message });
      setSelectedFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('document-upload') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
      onUploadSuccess?.();
      
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to upload document' });
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
      setTimeout(() => {
        setUploadProgress(0);
        setMessage(null);
      }, 3000);
    }
  };

  return (
    <Card>
      <Card.Header>
        <h5 className="mb-0">Upload Document</h5>
      </Card.Header>
      <Card.Body>
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Select file</Form.Label>
            <Form.Control
              id="document-upload"
              type="file"
              onChange={handleFileSelect}
              disabled={uploading}
              accept=".txt,.pdf,.doc,.docx,.md"
            />
            <Form.Text className="text-muted">
              Supported formats: TXT, PDF, DOC, DOCX, MD
            </Form.Text>
          </Form.Group>

          {selectedFile && (
            <div className="mb-3">
              <small className="text-muted">
                Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
              </small>
            </div>
          )}

          {uploading && (
            <div className="mb-3">
              <ProgressBar now={uploadProgress} label={`${uploadProgress}%`} />
            </div>
          )}

          {message && (
            <Alert variant={message.type === 'success' ? 'success' : 'danger'} className="mb-3">
              {message.text}
            </Alert>
          )}

          <Button
            variant="primary"
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload Document'}
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default DocumentUpload;