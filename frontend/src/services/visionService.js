import api from './api';

export const visionService = {
  async getLetters(language = 'Tamil') {
    const response = await api.get(`/vision/letters?language=${encodeURIComponent(language)}`);
    return response.data;
  },

  async getWritingLessons(language = 'Tamil') {
    const response = await api.get(`/vision/lessons?language=${encodeURIComponent(language)}`);
    return response.data;
  },

  async getCurriculum(language = 'Tamil', category = '', level = 0) {
    let url = `/vision/curriculum?language=${encodeURIComponent(language)}`;
    if (category) url += `&category=${encodeURIComponent(category)}`;
    if (level) url += `&level=${level}`;
    const response = await api.get(url);
    return response.data;
  },

  async getWritingStats() {
    const response = await api.get('/vision/stats');
    return response.data;
  },

  async evaluateCanvas(imageBlob, targetText = 'அ', mode = 'trace', language = 'Tamil', attemptNumber = 1, strokes = null) {
    const formData = new FormData();
    formData.append('file', imageBlob, 'handwriting.png');
    formData.append('target_text', targetText);
    formData.append('practice_mode', mode);
    formData.append('language', language);
    formData.append('attempt_number', attemptNumber);

    if (strokes) {
      formData.append('strokes_json', JSON.stringify(strokes));
    }

    const response = await api.post('/vision/evaluate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000,
    });
    return response.data;
  },

  async analyzeHandwriting(fileOrBlob, targetChar = '', mode = 'general', language = 'Tamil') {
    const formData = new FormData();
    formData.append('file', fileOrBlob, 'handwriting.png');
    if (targetChar) {
      formData.append('target_char', targetChar);
    }
    formData.append('mode', mode);
    formData.append('language', language);

    const response = await api.post('/vision/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 90000,
    });
    return response.data;
  }
};
