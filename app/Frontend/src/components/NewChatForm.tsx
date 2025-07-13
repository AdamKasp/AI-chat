import React, { useState } from 'react';
import { Form, Button, Spinner } from 'react-bootstrap';

interface NewChatFormProps {
  onSubmit: (prompt: string, model: string, systemPrompt?: string) => void;
  onCancel: () => void;
  loading: boolean;
}

const NewChatForm: React.FC<NewChatFormProps> = ({
  onSubmit,
  onCancel,
  loading,
}) => {
  const [prompt, setPrompt] = useState('');
  const [model, setModel] = useState('gemini-2.5-flash');
  const [systemPrompt, setSystemPrompt] = useState('');
  const [showSystemPrompt, setShowSystemPrompt] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit(prompt, model, systemPrompt.trim() || undefined);
    }
  };

  return (
    <div className="new-chat-form h-100 d-flex flex-column">
      <div className="mb-4">
        <h4 className="text-primary">🚀 Start New Chat</h4>
        <p className="text-muted">
          Ask me anything! I'm here to help with your questions.
        </p>
      </div>

      <Form onSubmit={handleSubmit} className="flex-grow-1 d-flex flex-column">
        <Form.Group className="mb-3">
          <Form.Label>Model</Form.Label>
          <Form.Select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            disabled={loading}
          >
            <option value="gemini-2.5-flash">gemini-2.5-flash</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <div className="d-flex justify-content-between align-items-center">
            <Form.Label>Your Message</Form.Label>
            <Button
              variant="outline-secondary"
              size="sm"
              onClick={() => setShowSystemPrompt(!showSystemPrompt)}
              disabled={loading}
            >
              {showSystemPrompt ? 'Hide' : 'Show'} System Prompt
            </Button>
          </div>
          <Form.Control
            as="textarea"
            rows={6}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your message here..."
            disabled={loading}
            required
          />
        </Form.Group>

        {showSystemPrompt && (
          <Form.Group className="mb-3">
            <Form.Label>System Prompt (Optional)</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={systemPrompt}
              onChange={(e) => setSystemPrompt(e.target.value)}
              placeholder="Enter system prompt to customize AI behavior..."
              disabled={loading}
            />
            <Form.Text className="text-muted">
              System prompts help customize how the AI responds to your questions.
            </Form.Text>
          </Form.Group>
        )}

        <div className="mt-auto">
          <div className="d-flex justify-content-end gap-2">
            <Button
              variant="outline-secondary"
              onClick={onCancel}
              disabled={loading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              disabled={loading || !prompt.trim()}
            >
              {loading ? (
                <>
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                    className="me-2"
                  />
                  Sending...
                </>
              ) : (
                'Send Message'
              )}
            </Button>
          </div>
        </div>
      </Form>
    </div>
  );
};

export default NewChatForm;