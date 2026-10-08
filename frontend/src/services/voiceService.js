import api, { API_BASE_URL } from './api';

export const voiceService = {
  async translateText(englishText, language = 'Tamil') {
    const response = await api.post('/voice/translate', {
      english_text: englishText,
      language: language
    });
    return response.data;
  },

  async analyzeVoice(audioBlob, expectedText = '', pronunciationGuide = '', originalEnglish = '', language = 'Tamil') {
    const formData = new FormData();
    formData.append('file', audioBlob, 'speech_recording.wav');
    formData.append('expected_text', expectedText);
    formData.append('pronunciation_guide', pronunciationGuide);
    formData.append('original_english', originalEnglish);
    formData.append('language', language);

    const response = await api.post('/voice/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000,
    });
    return response.data;
  },

  getSpeakAudioUrl(text, language = 'Tamil') {
    return `${API_BASE_URL}/voice/speak-get?text=${encodeURIComponent(text)}&language=${encodeURIComponent(language)}`;
  },

  async speakText(text, language = 'Tamil') {
    const response = await api.post(
      '/voice/speak',
      { text, language },
      { responseType: 'blob' }
    );
    return URL.createObjectURL(response.data);
  }
};
