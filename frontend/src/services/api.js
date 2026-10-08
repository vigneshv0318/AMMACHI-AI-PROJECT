import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 45000,
});

// Interceptor to inject JWT Bearer token into requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('ammachi_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if expired
      // localStorage.removeItem('ammachi_token');
    }
    return Promise.reject(error);
  }
);

export default api;
export { API_BASE_URL };
