import React, { useState, useRef, useEffect } from 'react';
import { 
  Mic, Square, Volume2, Sparkles, RefreshCw, ArrowLeft, CheckCircle2, 
  AlertCircle, HelpCircle, Globe, Play, BookOpen, MessageSquare, Award, RotateCcw
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { voiceService } from '../services/voiceService';
import { triggerCelebration } from '../components/common/Confetti';

const SUPPORTED_LANGUAGES = [
  { name: 'Tamil', native: 'தமிழ்', code: 'ta', flag: '🇮🇳' },
  { name: 'Telugu', native: 'తెలుగు', code: 'te', flag: '🇮🇳' },
  { name: 'Hindi', native: 'हिन्दी', code: 'hi', flag: '🇮🇳' }
];

const SAMPLE_PROMPTS = [
  "Hello, how are you?",
  "Thank you very much!",
  "Good morning!",
  "I love learning new words."
];

export const SpeakingPage = () => {
  const { currentLanguage, setLanguage } = useLanguage();
  const { refreshUser } = useAuth();

  const [selectedLanguage, setSelectedLanguage] = useState(currentLanguage || 'Tamil');
  const [englishInput, setEnglishInput] = useState('Hello, how are you?');
  const [translating, setTranslating] = useState(false);
  const [translationData, setTranslationData] = useState(null);

  // Audio Playback
  const [playingAudio, setPlayingAudio] = useState(false);

  // Audio Recording
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [micError, setMicError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);
  const audioPlayerRef = useRef(null);

  // Sync selectedLanguage with global context
  useEffect(() => {
    if (currentLanguage) {
      setSelectedLanguage(currentLanguage);
    }
  }, [currentLanguage]);

  // Clean up timers & recorder on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (audioPlayerRef.current) audioPlayerRef.current.pause();
    };
  }, []);

  const handleTranslate = async (textToTranslate = englishInput) => {
    const text = textToTranslate || englishInput;
    if (!text || !text.strip ? !text.trim() : !text) return;

    setTranslating(true);
    setAnalysisResult(null);
    setMicError(null);

    try {
      const data = await voiceService.translateText(text, selectedLanguage);
      setTranslationData(data);
    } catch (err) {
      console.error('Translation error:', err);
      // Fallback display if translation fails
      setTranslationData({
        original_text: text,
        translated_text: text,
        pronunciation_guide: text,
        language: selectedLanguage,
        language_code: selectedLanguage === 'Tamil' ? 'ta' : (selectedLanguage === 'Telugu' ? 'te' : 'hi')
      });
    } finally {
      setTranslating(false);
    }
  };

  const handlePlayAudio = async () => {
    if (!translationData?.translated_text || playingAudio) return;

    setPlayingAudio(true);
    try {
      const audioUrl = voiceService.getSpeakAudioUrl(
        translationData.translated_text, 
        translationData.language
      );

      if (audioPlayerRef.current) {
        audioPlayerRef.current.pause();
      }

      const audio = new Audio(audioUrl);
      audioPlayerRef.current = audio;

      audio.onended = () => setPlayingAudio(false);
      audio.onerror = () => setPlayingAudio(false);

      await audio.play();
    } catch (err) {
      console.warn('Audio playback note:', err);
      setPlayingAudio(false);
    }
  };

  const startRecording = async () => {
    setMicError(null);
    setAnalysisResult(null);
    try {
      audioChunksRef.current = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        stream.getTracks().forEach((track) => track.stop());
        await processAudio(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingSeconds(0);

      timerRef.current = setInterval(() => {
        setRecordingSeconds((prev) => prev + 1);
      }, 1000);
    } catch (err) {
      console.error('Microphone error:', err);
      setMicError('Microphone access denied. Please allow microphone permissions in your browser to practice speaking!');
    }
  };

  const stopRecording = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processAudio = async (audioBlob) => {
    setAnalyzing(true);
    try {
      const expectedText = translationData?.translated_text || '';
      const pronunciationGuide = translationData?.pronunciation_guide || '';
      const originalEnglish = translationData?.original_text || '';

      const result = await voiceService.analyzeVoice(
        audioBlob, 
        expectedText, 
        pronunciationGuide, 
        originalEnglish, 
        selectedLanguage
      );
      setAnalysisResult(result);

      if (result.recognition_status === 'CORRECT') {
        triggerCelebration();
      }
      refreshUser();
    } catch (err) {
      console.error('Voice analysis error:', err);
      setAnalysisResult({
        expected_text: translationData?.translated_text || '',
        detected_text: 'Audio received',
        recognition_status: 'UNCERTAIN',
        score: 30,
        confidence: 0.0,
        feedback: 'Aiyayo Kanna! I could not hear clearly. Please check your microphone and speak again in a quiet room!',
        mistake_explanation: 'Audio connection check required.',
        needs_retry: true,
        points_awarded: 0
      });
    } finally {
      setAnalyzing(false);
    }
  };

  const handleLanguageChange = (langName) => {
    setSelectedLanguage(langName);
    setLanguage(langName);
    if (translationData) {
      handleTranslate(englishInput);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      {/* Header Bar */}
      <div className="flex items-center justify-between bg-white/80 backdrop-blur border border-amber-200 rounded-3xl p-4 sm:p-5 shadow-sm">
        <div className="flex items-center gap-3">
          <Link
            to="/dashboard"
            className="p-2.5 rounded-2xl bg-amber-50 hover:bg-amber-100 text-amber-900 transition-all border border-amber-200"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-xl sm:text-2xl font-black text-amber-950 flex items-center gap-2">
              <span>Pronunciation Tutor</span>
              <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-300">
                AI Voice
              </span>
            </h1>
            <p className="text-xs text-stone-500 font-medium">
              Translate English sentences, listen to native speech, and perfect your pronunciation!
            </p>
          </div>
        </div>

        {/* Language Switcher */}
        <div className="flex items-center gap-1.5 bg-amber-50 p-1.5 rounded-2xl border border-amber-200">
          <Globe className="w-4 h-4 text-amber-700 ml-1 hidden sm:inline" />
          {SUPPORTED_LANGUAGES.map((lang) => (
            <button
              key={lang.name}
              onClick={() => handleLanguageChange(lang.name)}
              className={`px-3 py-1.5 rounded-xl text-xs font-extrabold transition-all ${
                selectedLanguage === lang.name
                  ? 'bg-amber-600 text-white shadow-sm'
                  : 'text-amber-900 hover:bg-amber-100'
              }`}
            >
              {lang.name}
            </button>
          ))}
        </div>
      </div>

      {/* STAGE 1: English Input & Language Selection */}
      <div className="bg-white border-2 border-amber-200 rounded-3xl p-5 sm:p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <label className="text-xs font-extrabold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
            <BookOpen className="w-4 h-4 text-amber-600" />
            <span>Stage 1: Enter English Word or Sentence</span>
          </label>
          <span className="text-xs font-bold text-stone-400">
            Target Language: <strong className="text-amber-800">{selectedLanguage}</strong>
          </span>
        </div>

        <div className="space-y-3">
          <div className="relative">
            <input
              type="text"
              value={englishInput}
              onChange={(e) => setEnglishInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleTranslate()}
              placeholder="Type an English word or sentence (e.g. Good morning!)..."
              className="w-full text-base sm:text-lg font-semibold px-4 py-3.5 rounded-2xl border-2 border-amber-200 focus:border-amber-500 focus:ring-4 focus:ring-amber-200/50 outline-none transition-all placeholder:text-stone-400"
            />
            {englishInput && (
              <button
                onClick={() => setEnglishInput('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-bold text-stone-400 hover:text-stone-600 bg-stone-100 px-2 py-1 rounded-lg"
              >
                Clear
              </button>
            )}
          </div>

          {/* Quick Prompts */}
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="text-[11px] font-bold text-stone-400">Quick Try:</span>
            {SAMPLE_PROMPTS.map((prompt) => (
              <button
                key={prompt}
                onClick={() => {
                  setEnglishInput(prompt);
                  handleTranslate(prompt);
                }}
                className="text-xs font-bold px-3 py-1 rounded-full bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 hover:border-amber-400 transition-all"
              >
                "{prompt}"
              </button>
            ))}
          </div>

          <button
            onClick={() => handleTranslate()}
            disabled={translating || !englishInput.trim()}
            className="w-full btn-primary py-3.5 text-base font-extrabold flex items-center justify-center gap-2 shadow-md disabled:opacity-50"
          >
            {translating ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                <span>Translating to {selectedLanguage}...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Translate & Learn Pronunciation 🚀</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* STAGE 2 & STAGE 3: Native Translation, Pronunciation Guide & Listen & Learn */}
      {translationData && (
        <div className="bg-gradient-to-br from-amber-50 via-white to-amber-100/40 border-2 border-amber-300 rounded-3xl p-6 shadow-sm space-y-6 animate-fade-in">
          <div className="flex items-center justify-between border-b border-amber-200 pb-3">
            <span className="text-xs font-extrabold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
              <Globe className="w-4 h-4 text-amber-600" />
              <span>Stage 2 & 3: Native Translation & Pronunciation Guide</span>
            </span>
            <span className="px-3 py-1 rounded-full bg-amber-200 text-amber-900 text-xs font-black">
              {translationData.language} ({translationData.language_code})
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Native Translation Card */}
            <div className="bg-white border-2 border-amber-200 rounded-2xl p-5 shadow-sm space-y-2">
              <span className="text-[11px] font-extrabold text-stone-400 uppercase tracking-wider block">
                Native Script Translation
              </span>
              <p className="text-2xl sm:text-3xl font-black text-amber-950 leading-relaxed font-sans">
                {translationData.translated_text}
              </p>
              <p className="text-xs text-stone-500 font-medium pt-1">
                English: "{translationData.original_text}"
              </p>
            </div>

            {/* Child-Friendly Pronunciation Guide Card */}
            <div className="bg-amber-100/70 border-2 border-amber-300 rounded-2xl p-5 shadow-sm space-y-2 flex flex-col justify-between">
              <div>
                <span className="text-[11px] font-extrabold text-amber-800 uppercase tracking-wider block flex items-center gap-1">
                  <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                  <span>Pronunciation Guide (Phonetics)</span>
                </span>
                <p className="text-xl sm:text-2xl font-extrabold text-amber-900 italic mt-1">
                  "{translationData.pronunciation_guide}"
                </p>
              </div>
              <p className="text-[11px] font-bold text-amber-700/80">
                Read the guide above to practice saying the phrase out loud!
              </p>
            </div>
          </div>

          {/* STAGE 3: Listen & Learn Button */}
          <div className="bg-white border border-amber-200 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3 text-left">
              <div className="p-3 rounded-2xl bg-amber-100 text-amber-800 shrink-0">
                <Volume2 className="w-6 h-6" />
              </div>
              <div>
                <h4 className="font-extrabold text-stone-900 text-sm">
                  Listen & Learn Native Pronunciation
                </h4>
                <p className="text-xs text-stone-500">
                  Powered by ElevenLabs emotive voice synthesis
                </p>
              </div>
            </div>

            <button
              onClick={handlePlayAudio}
              disabled={playingAudio}
              className={`w-full sm:w-auto px-6 py-3 rounded-2xl font-extrabold text-sm flex items-center justify-center gap-2 transition-all shadow-md ${
                playingAudio
                  ? 'bg-amber-200 text-amber-800 cursor-not-allowed'
                  : 'bg-amber-600 hover:bg-amber-700 text-white hover:scale-105 active:scale-95'
              }`}
            >
              {playingAudio ? (
                <>
                  <Volume2 className="w-5 h-5 animate-pulse" />
                  <span>Playing Audio...</span>
                </>
              ) : (
                <>
                  <Play className="w-5 h-5 fill-current" />
                  <span>Listen & Learn 🔊</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* STAGE 4: Your Turn 🎤 (Browser Microphone Recording) */}
      {translationData && (
        <div className="bg-white border-2 border-amber-200 rounded-3xl p-6 shadow-sm text-center space-y-5">
          <span className="text-xs font-extrabold text-amber-900 uppercase tracking-wider block">
            Stage 4: Your Turn 🎤 Speak in {selectedLanguage}
          </span>

          <div className="space-y-3">
            <p className="text-sm font-extrabold text-stone-800">
              Say: <strong className="text-amber-900 text-lg sm:text-xl font-black">"{translationData.translated_text}"</strong>
            </p>
            <p className="text-xs text-stone-500 max-w-md mx-auto">
              Press the big microphone button, speak clearly, and tap stop when done!
            </p>
          </div>

          {/* Big Microphone Button */}
          <div className="flex flex-col items-center justify-center gap-3 py-2">
            {!isRecording ? (
              <button
                onClick={startRecording}
                disabled={analyzing}
                className="w-24 h-24 sm:w-28 sm:h-28 rounded-full bg-gradient-to-br from-red-500 to-amber-600 hover:from-red-600 hover:to-amber-700 text-white flex flex-col items-center justify-center gap-1 shadow-lg hover:shadow-xl hover:scale-105 active:scale-95 transition-all group disabled:opacity-50"
              >
                <Mic className="w-10 h-10 group-hover:scale-110 transition-all" />
                <span className="text-[11px] font-black uppercase tracking-wider">Tap Mic</span>
              </button>
            ) : (
              <div className="flex flex-col items-center gap-3">
                <button
                  onClick={stopRecording}
                  className="w-24 h-24 sm:w-28 sm:h-28 rounded-full bg-red-600 text-white flex flex-col items-center justify-center gap-1 shadow-lg animate-pulse hover:scale-105 transition-all"
                >
                  <Square className="w-10 h-10 fill-current" />
                  <span className="text-[11px] font-black uppercase tracking-wider">Stop ({recordingSeconds}s)</span>
                </button>
                <div className="flex items-center gap-1 text-xs font-extrabold text-red-600 bg-red-50 px-3 py-1 rounded-full border border-red-200">
                  <span className="w-2 h-2 rounded-full bg-red-600 animate-ping mr-1" />
                  Recording your speech...
                </div>
              </div>
            )}

            {analyzing && (
              <div className="flex items-center gap-2 text-sm font-extrabold text-amber-800 bg-amber-50 px-4 py-2 rounded-2xl border border-amber-200">
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Evaluating speech with Deepgram STT...</span>
              </div>
            )}
          </div>

          {/* Mic Permission / Access Error */}
          {micError && (
            <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-800 text-xs font-bold flex items-center gap-2 max-w-md mx-auto">
              <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
              <span>{micError}</span>
            </div>
          )}
        </div>
      )}

      {/* STAGE 5 & 6: Recognition Status Result & Tutor Feedback */}
      {analysisResult && (
        <div className={`border-2 rounded-3xl p-6 shadow-sm space-y-5 animate-fade-in ${
          analysisResult.recognition_status === 'CORRECT'
            ? 'bg-emerald-50/90 border-emerald-300'
            : (analysisResult.recognition_status === 'NEEDS_PRACTICE'
                ? 'bg-amber-50/90 border-amber-300'
                : 'bg-sky-50/90 border-sky-300')
        }`}>
          {/* Status Header Badge */}
          <div className="flex flex-wrap items-center justify-between gap-2 border-b pb-3 border-stone-200">
            <div className="flex items-center gap-2.5">
              {analysisResult.recognition_status === 'CORRECT' && (
                <span className="p-2 rounded-xl bg-emerald-100 text-emerald-700">
                  <CheckCircle2 className="w-6 h-6" />
                </span>
              )}
              {analysisResult.recognition_status === 'NEEDS_PRACTICE' && (
                <span className="p-2 rounded-xl bg-amber-100 text-amber-800">
                  <AlertCircle className="w-6 h-6" />
                </span>
              )}
              {analysisResult.recognition_status === 'UNCERTAIN' && (
                <span className="p-2 rounded-xl bg-sky-100 text-sky-800">
                  <HelpCircle className="w-6 h-6" />
                </span>
              )}
              <div>
                <h3 className="text-lg font-black text-stone-900 flex items-center gap-2">
                  <span>Recognition Result:</span>
                  <span className={`px-3 py-0.5 rounded-full text-xs font-black uppercase tracking-wider ${
                    analysisResult.recognition_status === 'CORRECT'
                      ? 'bg-emerald-600 text-white'
                      : (analysisResult.recognition_status === 'NEEDS_PRACTICE'
                          ? 'bg-amber-500 text-white'
                          : 'bg-sky-600 text-white')
                  }`}>
                    {analysisResult.recognition_status}
                  </span>
                </h3>
                <p className="text-xs text-stone-500 font-medium">
                  Backend Evaluation Score: {analysisResult.score}/100 | Deepgram Conf: {analysisResult.confidence || '0.85'}
                </p>
              </div>
            </div>

            {analysisResult.points_awarded > 0 && (
              <span className="px-3.5 py-1.5 rounded-2xl bg-amber-500 text-white text-xs font-black flex items-center gap-1 shadow-sm">
                <Award className="w-4 h-4" />
                +{analysisResult.points_awarded} Points
              </span>
            )}
          </div>

          {/* Comparison Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
            <div className="bg-white p-4 rounded-2xl border border-stone-200">
              <span className="text-[10px] font-extrabold text-stone-400 uppercase tracking-wider block">
                Target Sentence
              </span>
              <p className="text-base font-extrabold text-stone-900 mt-0.5">
                {analysisResult.expected_text || translationData?.translated_text}
              </p>
            </div>

            <div className="bg-white p-4 rounded-2xl border border-stone-200">
              <span className="text-[10px] font-extrabold text-stone-400 uppercase tracking-wider block">
                Child Speech Detected (Deepgram STT)
              </span>
              <p className="text-base font-extrabold text-stone-900 mt-0.5">
                "{analysisResult.detected_text || 'No clear speech detected'}"
              </p>
            </div>
          </div>

          {/* Gemini AI Tutor Feedback Card */}
          <div className="bg-white p-5 rounded-2xl border-2 border-stone-200 space-y-2 text-left shadow-sm">
            <span className="text-xs font-extrabold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
              <MessageSquare className="w-4 h-4 text-amber-600" />
              <span>Native Language Tutor Feedback</span>
            </span>
            <p className="text-sm sm:text-base font-bold text-stone-800 leading-relaxed">
              {analysisResult.feedback}
            </p>
            {analysisResult.mistake_explanation && analysisResult.recognition_status === 'NEEDS_PRACTICE' && (
              <p className="text-xs font-extrabold text-amber-800 bg-amber-50 p-2.5 rounded-xl border border-amber-200 mt-2">
                💡 Tip: {analysisResult.mistake_explanation}
              </p>
            )}
          </div>

          {/* Practice Controls (Listen Again / Try Again / New Sentence) */}
          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <button
              onClick={handlePlayAudio}
              className="btn-secondary text-xs sm:text-sm px-5 py-2.5 flex items-center gap-2"
            >
              <Volume2 className="w-4 h-4" />
              <span>Listen Again 🔊</span>
            </button>

            <button
              onClick={startRecording}
              className="btn-primary text-xs sm:text-sm px-6 py-2.5 flex items-center gap-2 shadow-md"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Try Again 🎤</span>
            </button>

            <button
              onClick={() => {
                setEnglishInput('');
                setTranslationData(null);
                setAnalysisResult(null);
              }}
              className="px-5 py-2.5 rounded-2xl bg-stone-100 hover:bg-stone-200 text-stone-800 text-xs sm:text-sm font-extrabold transition-all border border-stone-200"
            >
              New Sentence ✏️
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
