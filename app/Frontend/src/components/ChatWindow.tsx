import React, { useState, useRef, useEffect } from 'react';
import { Card, Badge, Form, Button, Spinner } from 'react-bootstrap';
import { ChatResponse, Message } from '../types/chat';

interface ChatWindowProps {
  chat: ChatResponse;
  onSendMessage?: (message: string) => void;
  loading?: boolean;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ chat, onSendMessage, loading = false }) => {
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat.messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && onSendMessage && !loading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };
  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const renderMessage = (message: Message, index: number) => {
    const isUser = message.author === 'user';
    
    return (
      <div key={message.id} className={`message-container ${isUser ? 'user-message' : 'ai-message'} mb-3`}>
        <div className={`d-flex ${isUser ? 'justify-content-end' : 'justify-content-start'}`}>
          <Card className={`message-bubble ${isUser ? 'user-bubble' : 'ai-bubble'} shadow-sm`}>
            <Card.Body className="p-3">
              {!isUser && (
                <div className="d-flex align-items-center mb-2">
                  <div className="ai-avatar me-2">🤖</div>
                  <Badge bg="primary" className="ai-badge">
                    AI Assistant
                  </Badge>
                </div>
              )}
              <div className={isUser ? 'user-message-text' : 'ai-response'}>
                {message.message.split('\n').map((line, lineIndex) => (
                  <p key={lineIndex} className="mb-2">
                    {line}
                  </p>
                ))}
              </div>
              <div className={`message-time ${isUser ? 'text-end' : 'text-start'} mt-2`}>
                <small className="text-muted">
                  {formatTime(message.created_at)}
                </small>
              </div>
            </Card.Body>
          </Card>
        </div>
      </div>
    );
  };

  return (
    <div className="chat-window h-100 d-flex flex-column">
      <div className="chat-messages flex-grow-1 overflow-auto">
        {chat.messages && chat.messages.length > 0 ? (
          chat.messages.map((message, index) => renderMessage(message, index))
        ) : (
          <div className="text-center text-muted mt-4">
            <p>No messages yet. Start a conversation!</p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input Form */}
      {onSendMessage && (
        <div className="border-top pt-3">
          <Form onSubmit={handleSubmit}>
            <div className="d-flex gap-2">
              <Form.Control
                type="text"
                placeholder="Type your message..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                disabled={loading}
                className="flex-grow-1"
              />
              <Button
                type="submit"
                variant="primary"
                disabled={loading || !message.trim()}
                style={{ minWidth: '100px' }}
              >
                {loading ? (
                  <>
                    <Spinner size="sm" className="me-2" />
                    Sending...
                  </>
                ) : (
                  'Send'
                )}
              </Button>
            </div>
          </Form>
        </div>
      )}

      {/* Chat Info */}
      <div className="chat-info border-top pt-3 mt-2">
        <div className="d-flex justify-content-between align-items-center text-muted">
          <small>
            <strong>Chat ID:</strong> {chat.id.substring(0, 8)}...
          </small>
          <small>
            <strong>Messages:</strong> {chat.messages ? chat.messages.length : 0}
          </small>
          <small>
            <strong>Last Updated:</strong> {chat.updated_at ? formatTime(chat.updated_at) : formatTime(chat.created_at)}
          </small>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;