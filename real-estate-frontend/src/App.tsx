// src/App.tsx
import React, { useEffect } from 'react';
import { BrowserRouter as Router, useNavigate } from 'react-router-dom';
import { setNavigate } from './utils/apiClient';
import Routes from './Routes';
import Navbar from './components/Navbar';

const AppContent = () => {
  const navigate = useNavigate();
  
  useEffect(() => {
    setNavigate(navigate);
  }, [navigate]);

  return (
    <div>
      <Navbar />
      <Routes />
    </div>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;