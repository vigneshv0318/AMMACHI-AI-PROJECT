import React, { useState } from 'react';
import { Volume2, VolumeX, Sparkles } from 'lucide-react';
import { voiceService } from '../../services/voiceService';
import { useLanguage } from '../../context/LanguageContext';

export const SpeechBubble = ({
  text,
  title = "Ammachi says:",
  autoPlay = false,
  className = "",
  showAudio = true
}) => {
  const { currentLanguage, activeLangMeta } = useLanguage();
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioObj, setAudioObj] = useState(null);

  const handlePlayAudio = () => {
    if (isPlaying && audioObj) {
      audioObj.pause();
      setIsPlaying(false);
      return;
    }

    try {
      const url = voiceService.getSpeakAudioUrl(text, currentLanguage);
      const audio = new Audio(url);
      setAudioObj(audio);
      setIsPlaying(true);

      audio.onended = () => setIsPlaying(false);
      audio.onerror = () => setIsPlaying(false);
      audio.play().catch((err) => {
        console.warn("Audio playback issue:", err);
        setIsPlaying(false);
      });
    } catch (e) {
      console.warn("Speech playback error:", e);
      setIsPlaying(false);
    }
  };

  return (
    <div className={`ammachi-bubble ${className}`}>
      <div className="flex items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-1.5 font-bold text-amber-900 text-sm sm:text-base">
          <Sparkles className="w-4 h-4 text-amber-500 fill-amber-400" />
          <span>{title || `${activeLangMeta.persona.split(' ')[0]} says:`}</span>
        </div>
        {showAudio && (
          <button
            onClick={handlePlayAudio}
            type="button"
            className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-200/70 hover:bg-amber-300 text-amber-900 text-xs font-semibold active:scale-95 transition-all shadow-sm"
            title="Listen to Ammachi"
          >
            {isPlaying ? (
              <>
                <VolumeX className="w-3.5 h-3.5 text-orange-600 animate-pulse" />
                <span>Pause</span>
              </>
            ) : (
              <>
                <Volume2 className="w-3.5 h-3.5 text-amber-800" />
                <span>Listen 🔊</span>
              </>
            )}
          </button>
        )}
      </div>
      <p className="text-stone-800 text-base sm:text-lg leading-relaxed font-medium">
        {text}
      </p>
    </div>
  );
};
