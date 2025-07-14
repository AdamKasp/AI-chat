import React, { useState, useEffect } from 'react';
import { ListGroup, Badge, Button } from 'react-bootstrap';
import { ChatResponse } from '../types/chat';
import { UserResponse } from '../types/user';
import { userApi } from '../services/userApi';

interface ChatListProps {
  chats: ChatResponse[];
  selectedChat: ChatResponse | null;
  onChatSelect: (chatId: string) => void;
  onChatDelete?: (chatId: string) => void;
  loading: boolean;
}

const ChatList: React.FC<ChatListProps> = ({
  chats,
  selectedChat,
  onChatSelect,
  onChatDelete,
  loading,
}) => {
  const [users, setUsers] = useState<{ [key: string]: UserResponse }>({});

  // Load user data for chats
  useEffect(() => {
    const loadUsers = async () => {
      const userIds = Array.from(new Set(chats.map(chat => chat.user_id)));
      const newUsers: { [key: string]: UserResponse } = { ...users };

      for (const userId of userIds) {
        if (!newUsers[userId]) {
          try {
            const user = await userApi.getUser(userId);
            newUsers[userId] = user;
          } catch (error) {
            console.error(`Failed to load user ${userId}:`, error);
            // Create placeholder user if API call fails
            newUsers[userId] = {
              id: userId,
              login: 'Unknown User',
              created_at: new Date().toISOString(),
              updated_at: null,
            };
          }
        }
      }

      setUsers(newUsers);
    };

    if (chats.length > 0) {
      loadUsers();
    }
  }, [chats]);

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return date.toLocaleDateString();
  };

  const truncateText = (text: string | undefined, maxLength: number = 60) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const getLastUserMessage = (chat: ChatResponse) => {
    const userMessages = chat.messages?.filter(msg => msg.author === 'user') || [];
    return userMessages.length > 0 ? userMessages[userMessages.length - 1].message : '';
  };

  const getLastAgentResponse = (chat: ChatResponse) => {
    const agentMessages = chat.messages?.filter(msg => msg.author === 'agent') || [];
    return agentMessages.length > 0 ? agentMessages[agentMessages.length - 1].message : '';
  };

  const getMessageCount = (chat: ChatResponse) => {
    return chat.messages?.length || 0;
  };

  if (!chats || chats.length === 0) {
    if (loading) {
      return (
        <div className="p-4 text-center text-muted">
          <div className="mb-3">⏳</div>
          <p>Loading chats...</p>
        </div>
      );
    }
    return (
      <div className="p-4 text-center text-muted">
        <div className="mb-3">📝</div>
        <p>No chats yet. Start a new conversation!</p>
      </div>
    );
  }

  return (
    <ListGroup variant="flush" className="chat-list">
      {chats.filter(chat => chat && chat.id).map((chat) => (
        <ListGroup.Item
          key={chat.id}
          action
          active={selectedChat?.id === chat.id}
          className="chat-list-item border-0 position-relative"
          style={{ cursor: 'pointer' }}
        >
          <div 
            className="d-flex flex-column"
            onClick={() => onChatSelect(chat.id)}
          >
            <div className="d-flex justify-content-between align-items-start mb-1">
              <h6 className="mb-0 chat-title">
                {truncateText(getLastUserMessage(chat)) || 'Untitled Chat'}
              </h6>
              <div className="d-flex align-items-center">
                <Badge bg="light" text="muted" className="ms-2">
                  {formatTime(chat.updated_at || chat.created_at)}
                </Badge>
                {onChatDelete && (
                  <Button
                    variant="link"
                    size="sm"
                    className="text-danger p-0 ms-2"
                    onClick={(e) => {
                      e.stopPropagation();
                      if (window.confirm('Are you sure you want to delete this chat?')) {
                        onChatDelete(chat.id);
                      }
                    }}
                    title="Delete chat"
                  >
                    <i className="bi bi-trash"></i>
                  </Button>
                )}
              </div>
            </div>
            <div className="d-flex justify-content-between align-items-center mb-1">
              <small className="text-primary">
                <i className="bi bi-person-circle me-1"></i>
                {users[chat.user_id]?.login || 'Loading...'}
              </small>
              <small className="text-muted">
                💬 {getMessageCount(chat)} messages
              </small>
            </div>
            <p className="mb-0 text-muted chat-preview">
              {truncateText(getLastAgentResponse(chat), 80) || 'No response yet'}
            </p>
          </div>
        </ListGroup.Item>
      ))}
    </ListGroup>
  );
};

export default ChatList;