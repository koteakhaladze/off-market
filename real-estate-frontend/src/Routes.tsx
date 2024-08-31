// src/Routes.tsx
import React from 'react';
import { Route, Routes } from 'react-router-dom';
import RequireAuth from './components/RequireAuth';
import PropertyList from './components/PropertyList';
import PropertyDetail from './components/PropertyDetail';
import Login from './components/Login';
import Signup from './components/Signup';
import Profile from './components/Profile';

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<PropertyList />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route 
        path="/property/:id" 
        element={
          <RequireAuth>
            <PropertyDetail />
          </RequireAuth>
        } 
      />
      <Route 
        path="/profile" 
        element={
          <RequireAuth>
            <Profile />
          </RequireAuth>
        } 
      />
    </Routes>
  );
};

export default AppRoutes;