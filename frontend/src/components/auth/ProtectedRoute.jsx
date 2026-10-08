import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-warmbg text-amber-900 space-y-4">
        <div className="text-6xl animate-bounce">👵</div>
        <p className="text-lg font-black tracking-tight">Opening Ammachi's Classroom...</p>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/auth" replace />;
  }

  return children;
};
