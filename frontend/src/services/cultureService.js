import api from './api';

export const cultureService = {
  async getFestivals(language = 'Tamil') {
    const response = await api.get(`/culture/festivals?language=${encodeURIComponent(language)}`);
    return response.data;
  },

  async getFestivalVideos(festival = 'pongal', language = 'Tamil') {
    const response = await api.get(`/culture/videos?festival=${encodeURIComponent(festival)}&language=${encodeURIComponent(language)}`);
    return response.data;
  },

  async getFestivalQuiz(festival = 'pongal', language = 'Tamil') {
    const response = await api.get(`/culture/quiz?festival=${encodeURIComponent(festival)}&language=${encodeURIComponent(language)}`);
    return response.data;
  },

  async submitQuizAnswer(payload) {
    const response = await api.post('/culture/quiz/submit', payload);
    return response.data;
  },

  async sendCultureChat(message, history = [], language = 'Tamil') {
    const response = await api.post('/culture/chat', {
      message,
      history: JSON.stringify(history),
      language,
    }, {
      timeout: 60000
    });
    return response.data;
  }
};
