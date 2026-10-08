import React, { createContext, useContext, useState, useEffect } from 'react';
import { userService } from '../services/userService';
import { useAuth } from './AuthContext';

const LanguageContext = createContext(null);

export const SUPPORTED_LANGUAGES = [
  { id: 'Tamil', name: 'Tamil', nativeName: 'தமிழ்', scriptFont: 'font-tamil', greeting: 'வணக்கம் (Vanakkam)', persona: 'Ammachi (அம்மாச்சி)' },
  { id: 'Telugu', name: 'Telugu', nativeName: 'తెలుగు', scriptFont: 'font-telugu', greeting: 'నమస్కారం (Namaskaram)', persona: 'Ammamma (అమ్మమ్మ)' },
  { id: 'Hindi', name: 'Hindi', nativeName: 'हिन्दी', scriptFont: 'font-sans', greeting: 'नमस्ते (Namaste)', persona: 'Dadi (दादी)' },
];

export const LanguageProvider = ({ children }) => {
  const { user } = useAuth();
  const [currentLanguage, setCurrentLanguage] = useState(
    localStorage.getItem('ammachi_language') || user?.current_language || 'Tamil'
  );

  useEffect(() => {
    if (user?.current_language && user.current_language !== currentLanguage) {
      setCurrentLanguage(user.current_language);
    }
  }, [user]);

  const setLanguage = async (lang) => {
    setCurrentLanguage(lang);
    localStorage.setItem('ammachi_language', lang);
    try {
      if (user) {
        await userService.updateLanguage(lang);
      }
    } catch (e) {
      console.warn('Language update backend sync error:', e);
    }
  };

  const activeLangMeta = SUPPORTED_LANGUAGES.find(l => l.id.toLowerCase() === currentLanguage.toLowerCase()) || SUPPORTED_LANGUAGES[0];

  return (
    <LanguageContext.Provider
      value={{
        currentLanguage,
        setLanguage,
        activeLangMeta,
        languages: SUPPORTED_LANGUAGES
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
