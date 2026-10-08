import api from './api';

export const authService = {
  async login(username, password) {
    const response = await api.post('/login', { username, password });
    return response.data;
  },

  async signup(username, password, language = 'Tamil') {
    const response = await api.post('/signup', { username, password, language });
    return response.data;
  },

  async googleAuth(idToken) {
    const response = await api.post('/auth/google', { id_token: idToken });
    return response.data;
  },

  async getAuthConfig() {
    const response = await api.get('/auth/config');
    return response.data;
  },

  async getMe() {
    const response = await api.get('/me');
    return response.data;
  }
};
