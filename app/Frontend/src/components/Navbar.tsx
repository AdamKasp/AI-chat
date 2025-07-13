import React from 'react';
import { Navbar as BSNavbar, Nav, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import UserSelector from './UserSelector';
import { UserResponse } from '../types/user';

interface NavbarProps {
  selectedUser: UserResponse | null;
  onUserSelect: (user: UserResponse) => void;
}

const Navbar: React.FC<NavbarProps> = ({ selectedUser, onUserSelect }) => {
  return (
    <BSNavbar expand="lg" className="custom-navbar shadow-sm" fixed="top">
      <Container>
        <BSNavbar.Brand as={Link} to="/" className="fw-bold text-white">
          AI Agent Dashboard
        </BSNavbar.Brand>
        <BSNavbar.Toggle aria-controls="basic-navbar-nav" />
        <BSNavbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/chat" className="text-white-50">
              💬 Chat
            </Nav.Link>
            <Nav.Link as={Link} to="/documents" className="text-white-50">
              📄 Documents
            </Nav.Link>
            <Nav.Link as={Link} to="/rag" className="text-white-50">
              🔍 RAG Search
            </Nav.Link>
          </Nav>
          <Nav className="ms-3">
            <UserSelector 
              selectedUser={selectedUser}
              onUserSelect={onUserSelect}
            />
          </Nav>
        </BSNavbar.Collapse>
      </Container>
    </BSNavbar>
  );
};

export default Navbar;