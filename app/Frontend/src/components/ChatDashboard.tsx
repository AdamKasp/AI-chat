import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Alert, Spinner } from 'react-bootstrap';
import ChatList from './ChatList';
import ChatWindow from './ChatWindow';
import NewChatForm from './NewChatForm';
import { ChatResponse } from '../types/chat';
import { UserResponse } from '../types/user';
import { chatApi } from '../services/chatApi';

interface ChatDashboardProps {
  selectedUser: UserResponse | null;
}

const ChatDashboard: React.FC<ChatDashboardProps> = ({ selectedUser }) => {
  const [chats, setChats] = useState<ChatResponse[]>([]);
  const [selectedChat, setSelectedChat] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showNewChatForm, setShowNewChatForm] = useState(false);

  const loadChats = async () => {
    if (!selectedUser) {
      setChats([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await chatApi.getChats(100, 0, selectedUser.id);
      setChats(response.chats);
    } catch (err) {
      setError('Failed to load chats. Please try again.');
      console.error('Error loading chats:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChatSelect = async (chatId: string) => {
    try {
      setLoading(true);
      const chat = await chatApi.getChat(chatId);
      setSelectedChat(chat);
    } catch (err) {
      setError('Failed to load chat. Please try again.');
      console.error('Error loading chat:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = async (prompt: string, model: string, systemPrompt?: string) => {
    if (!selectedUser) {
      setError('Please select a user first.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await chatApi.createChat({
        user_id: selectedUser.id,
        prompt,
        model,
        system_prompt: systemPrompt,
      });
      
      // Get the full chat details using the chat_id from response
      const chatId = response.metadata.chat_id;
      const fullChat = await chatApi.getChat(chatId);
      
      setChats([fullChat, ...chats]);
      setSelectedChat(fullChat);
      setShowNewChatForm(false);
    } catch (err) {
      setError('Failed to create chat. Please try again.');
      console.error('Error creating chat:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (message: string) => {
    if (!selectedUser || !selectedChat) {
      setError('Please select a user and chat first.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      await chatApi.continueChat(selectedChat.id, message, selectedUser.id);
      
      // Refresh the current chat to get updated messages
      const updatedChat = await chatApi.getChat(selectedChat.id);
      setSelectedChat(updatedChat);
      
      // Update the chat in the list as well
      setChats(prevChats => 
        prevChats.map(chat => 
          chat.id === selectedChat.id ? updatedChat : chat
        )
      );
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Error sending message:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteChat = async (chatId: string) => {
    try {
      setLoading(true);
      setError(null);
      
      await chatApi.deleteChat(chatId);
      
      // Remove the deleted chat from the list
      setChats(prevChats => prevChats.filter(chat => chat.id !== chatId));
      
      // If the deleted chat was selected, clear the selection
      if (selectedChat?.id === chatId) {
        setSelectedChat(null);
      }
    } catch (err) {
      setError('Failed to delete chat. Please try again.');
      console.error('Error deleting chat:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadChats();
  }, [selectedUser]);

  return (
    <Container fluid className="mt-5 pt-3">
      <Row className="g-3">
        <Col lg={4} className="d-flex flex-column">
          <Card className="shadow-sm h-100">
            <Card.Header className="bg-gradient-primary text-white d-flex justify-content-between align-items-center">
              <h5 className="mb-0">💬 Chat History</h5>
              <button
                className="btn btn-outline-light btn-sm"
                onClick={() => setShowNewChatForm(true)}
                disabled={loading}
              >
                + New Chat
              </button>
            </Card.Header>
            <Card.Body className="p-0">
              {error && (
                <Alert variant="danger" className="m-3 mb-0">
                  {error}
                </Alert>
              )}
              {loading && (
                <div className="d-flex justify-content-center align-items-center p-4">
                  <Spinner animation="border" size="sm" className="me-2" />
                  <span>Loading...</span>
                </div>
              )}
              <ChatList
                chats={chats}
                selectedChat={selectedChat}
                onChatSelect={handleChatSelect}
                onChatDelete={handleDeleteChat}
                loading={loading}
              />
            </Card.Body>
          </Card>
        </Col>
        
        <Col lg={8}>
          <Card className="shadow-sm">
            <Card.Header className="bg-gradient-primary text-white">
              <h5 className="mb-0">
                {selectedChat ? 'Chat Conversation' : 'Welcome to AI Agent'}
              </h5>
            </Card.Header>
            <Card.Body style={{ height: '600px' }}>
              {showNewChatForm ? (
                <NewChatForm
                  onSubmit={handleNewChat}
                  onCancel={() => setShowNewChatForm(false)}
                  loading={loading}
                />
              ) : selectedChat ? (
                <ChatWindow 
                  chat={selectedChat} 
                  onSendMessage={handleSendMessage}
                  onDeleteChat={() => handleDeleteChat(selectedChat.id)}
                  loading={loading}
                />
              ) : (
                <div className="d-flex flex-column align-items-center justify-content-center h-100 text-center">
                  <div className="mb-4">
                    <div className="chat-welcome-icon">🤖</div>
                  </div>
                  <h4 className="text-muted">Welcome to AI Agent Dashboard</h4>
                  <p className="text-muted">
                    Select a chat from the history or create a new one to get started.
                  </p>
                  <button
                    className="btn btn-primary"
                    onClick={() => setShowNewChatForm(true)}
                  >
                    Start New Chat
                  </button>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ChatDashboard;