import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('ammachi_token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem('ammachi_token');
      if (savedToken) {
        try {
          const profile = await authService.getMe();
          setUser(profile);
          setToken(savedToken);
        } catch (error) {
          console.warn('Session token validation failed, clearing session:', error);
          localStorage.removeItem('ammachi_token');
          setToken(null);
          setUser(null);
        }
      } else {
        setToken(null);
        setUser(null);
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (username, password) => {
    const data = await authService.login(username, password);
    if (data.token) {
      localStorage.setItem('ammachi_token', data.token);
      setToken(data.token);
      setUser({ username: data.username, points: data.points, current_language: data.language });
    }
    return data;
  };

  const signup = async (username, password, language = 'Tamil') => {
    const data = await authService.signup(username, password, language);
    if (data.token) {
      localStorage.setItem('ammachi_token', data.token);
      setToken(data.token);
      setUser({ username: data.username, points: data.points, current_language: data.language });
    }
    return data;
  };

  const googleLogin = async (idToken) => {
    const data = await authService.googleAuth(idToken);
    if (data.token) {
      localStorage.setItem('ammachi_token', data.token);
      setToken(data.token);
      setUser({ username: data.username, points: data.points, current_language: data.language });
    }
    return data;
  };

  const logout = () => {
    localStorage.removeItem('ammachi_token');
    setToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    try {
      const profile = await authService.getMe();
      setUser(profile);
    } catch (e) {
      console.error('Failed to refresh user:', e);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated: !!user,
        login,
        signup,
        googleLogin,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
