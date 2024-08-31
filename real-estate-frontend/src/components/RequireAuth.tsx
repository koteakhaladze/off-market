// src/components/RequireAuth.tsx
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

const RequireAuth: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const location = useLocation();
  const token = localStorage.getItem('token');

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

export default RequireAuth;