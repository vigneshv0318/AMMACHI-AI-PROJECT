import { API_BASE_URL } from '../../services/api';

/** Maps Ammachi language names to BCP-47 codes for Web Speech fallback. */
export const TTS_LANG_CODES = {
  Tamil: 'ta-IN',
  Telugu: 'te-IN',
  Hindi: 'hi-IN',
  Malayalam: 'ml-IN',
  Kannada: 'kn-IN',
};

/** Backend TTS endpoint for a native phrase (falls back to speechSynthesis in the caller). */
export const languageToTts = (text, language = 'Tamil') =>
  `${API_BASE_URL}/voice/speak-get?text=${encodeURIComponent(text)}&language=${encodeURIComponent(language)}`;
