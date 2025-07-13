import React, { useState, useEffect } from 'react';
import { Dropdown, Button, Modal, Form, Alert, Badge } from 'react-bootstrap';
import { UserResponse, UserCreateRequest } from '../types/user';
import { userApi } from '../services/userApi';

interface UserSelectorProps {
  selectedUser: UserResponse | null;
  onUserSelect: (user: UserResponse) => void;
}

const UserSelector: React.FC<UserSelectorProps> = ({ selectedUser, onUserSelect }) => {
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [newUserLogin, setNewUserLogin] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [createLoading, setCreateLoading] = useState<boolean>(false);

  // Load users on component mount
  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const response = await userApi.getUsers(100, 0);
      setUsers(response.users);
      
      // If no user is selected and we have users, select the first one
      if (!selectedUser && response.users.length > 0) {
        onUserSelect(response.users[0]);
      }
    } catch (err) {
      console.error('Failed to load users:', err);
      setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async () => {
    if (!newUserLogin.trim()) {
      setError('Login is required');
      return;
    }

    setCreateLoading(true);
    setError('');

    try {
      const newUser = await userApi.createUser({ login: newUserLogin.trim() });
      setUsers([newUser, ...users]); // Add to beginning of list
      onUserSelect(newUser); // Select the newly created user
      setShowCreateModal(false);
      setNewUserLogin('');
    } catch (err) {
      console.error('Failed to create user:', err);
      setError('Failed to create user. Login might already exist.');
    } finally {
      setCreateLoading(false);
    }
  };

  const formatUserDisplay = (user: UserResponse) => {
    const date = new Date(user.created_at);
    return `${user.login} (${date.toLocaleDateString()})`;
  };

  if (loading) {
    return (
      <div className="d-flex align-items-center">
        <div className="spinner-border spinner-border-sm me-2" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <span>Loading users...</span>
      </div>
    );
  }

  return (
    <>
      <div className="d-flex align-items-center">
        <Dropdown>
          <Dropdown.Toggle variant="outline-primary" id="user-selector">
            <i className="bi bi-person-circle me-2"></i>
            {selectedUser ? selectedUser.login : 'Select User'}
          </Dropdown.Toggle>

          <Dropdown.Menu>
            <Dropdown.Header>Select User</Dropdown.Header>
            {users.map((user) => (
              <Dropdown.Item
                key={user.id}
                active={selectedUser?.id === user.id}
                onClick={() => onUserSelect(user)}
              >
                <div className="d-flex flex-column">
                  <strong>{user.login}</strong>
                  <small className="text-muted">
                    Created: {new Date(user.created_at).toLocaleDateString()}
                  </small>
                </div>
              </Dropdown.Item>
            ))}
            
            {users.length === 0 && (
              <Dropdown.Item disabled>No users found</Dropdown.Item>
            )}
            
            <Dropdown.Divider />
            <Dropdown.Item onClick={() => setShowCreateModal(true)}>
              <i className="bi bi-plus-circle me-2"></i>
              Create New User
            </Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>

        {selectedUser && (
          <Badge bg="secondary" className="ms-2">
            ID: {selectedUser.id.substring(0, 8)}...
          </Badge>
        )}
      </div>

      {/* Create User Modal */}
      <Modal show={showCreateModal} onHide={() => setShowCreateModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Create New User</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error && (
            <Alert variant="danger" onClose={() => setError('')} dismissible>
              {error}
            </Alert>
          )}
          
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Login</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                value={newUserLogin}
                onChange={(e) => setNewUserLogin(e.target.value)}
                disabled={createLoading}
              />
              <Form.Text className="text-muted">
                This will be used to identify the user in chats.
              </Form.Text>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button 
            variant="secondary" 
            onClick={() => setShowCreateModal(false)}
            disabled={createLoading}
          >
            Cancel
          </Button>
          <Button 
            variant="primary" 
            onClick={handleCreateUser}
            disabled={createLoading || !newUserLogin.trim()}
          >
            {createLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status">
                  <span className="visually-hidden">Loading...</span>
                </span>
                Creating...
              </>
            ) : (
              'Create User'
            )}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default UserSelector;