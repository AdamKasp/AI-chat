import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import ChatDashboard from './components/ChatDashboard';
import DocumentDashboard from './components/DocumentDashboard';
import RAGDashboard from './components/RAGDashboard';
import Navbar from './components/Navbar';
import { UserResponse } from './types/user';

function App() {
  const [selectedUser, setSelectedUser] = useState<UserResponse | null>(null);

  const handleUserSelect = (user: UserResponse) => {
    setSelectedUser(user);
  };

  return (
    <Router>
      <div className="App">
        <Navbar 
          selectedUser={selectedUser}
          onUserSelect={handleUserSelect}
        />
        <Routes>
          <Route path="/" element={<ChatDashboard selectedUser={selectedUser} />} />
          <Route path="/chat" element={<ChatDashboard selectedUser={selectedUser} />} />
          <Route path="/documents" element={<DocumentDashboard />} />
          <Route path="/rag" element={<RAGDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
