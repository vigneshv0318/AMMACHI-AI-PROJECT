import React, { useState, useEffect } from 'react';
import { Sparkles, Send, Award, BookOpen, Film, Image as ImageIcon, CheckCircle, RefreshCw, ArrowLeft, Play, Youtube, HelpCircle, Check, X, Flame, ChevronRight, RotateCcw, Trophy } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { cultureService } from '../services/cultureService';
import { triggerCelebration } from '../components/common/Confetti';
import { AmmachiMascot } from '../components/common/AmmachiMascot';

export const CulturePage = () => {
  const { currentLanguage } = useLanguage();
  const { user, refreshUser } = useAuth();

  const [festivals, setFestivals] = useState([]);
  const [selectedFestival, setSelectedFestival] = useState(null);
  const [activeTab, setActiveTab] = useState('video'); // 'video' | 'quiz' | 'story'
  
  // Videos
  const [activeVideo, setActiveVideo] = useState(null);
  const [festivalVideos, setFestivalVideos] = useState([]);
  const [loadingVideos, setLoadingVideos] = useState(false);

  // Gamified Quiz State
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [submittedResult, setSubmittedResult] = useState(null);
  const [submittingAnswer, setSubmittingAnswer] = useState(false);
  const [quizScore, setQuizScore] = useState(0);
  const [quizStreak, setQuizStreak] = useState(0);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [loadingQuiz, setLoadingQuiz] = useState(false);

  // Chat Storytelling
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loadingChat, setLoadingChat] = useState(false);
  const [userStamps, setUserStamps] = useState([]);

  // Load festivals for selected language
  useEffect(() => {
    const fetchFestivals = async () => {
      try {
        const list = await cultureService.getFestivals(currentLanguage);
        setFestivals(list);
        if (list && list.length > 0) {
          handleSelectFestival(list[0]);
        }
      } catch (err) {
        console.error('Failed to load festivals:', err);
      }
    };
    fetchFestivals();
  }, [currentLanguage]);

  const loadQuiz = async (festivalId) => {
    setLoadingQuiz(true);
    setCurrentQuestionIndex(0);
    setSelectedOption(null);
    setSubmittedResult(null);
    setQuizScore(0);
    setQuizStreak(0);
    setQuizCompleted(false);
    try {
      const questions = await cultureService.getFestivalQuiz(festivalId, currentLanguage);
      setQuizQuestions(questions || []);
    } catch (err) {
      console.error('Error loading quiz:', err);
    } finally {
      setLoadingQuiz(false);
    }
  };

  const handleSelectFestival = async (festival) => {
    setSelectedFestival(festival);
    
    // 1. Load Videos
    if (festival.videos && festival.videos.length > 0) {
      setFestivalVideos(festival.videos);
      setActiveVideo(festival.videos[0]);
    } else {
      setLoadingVideos(true);
      try {
        const vids = await cultureService.getFestivalVideos(festival.id, currentLanguage);
        setFestivalVideos(vids || []);
        setActiveVideo(vids && vids.length > 0 ? vids[0] : null);
      } catch (err) {
        console.error('Failed to load videos:', err);
      } finally {
        setLoadingVideos(false);
      }
    }

    // 2. Load 10-Question Gamified Quiz
    loadQuiz(festival.id);

    // 3. Reset chat greeting
    setMessages([
      {
        role: 'assistant',
        content: `Vanakkam Kanna! I am so excited to explore ${festival.name} (${festival.native_name}) with you! Watch the video story and take the 10-question quiz to earn points and your Cultural Stamp!`,
        videos: festival.videos
      }
    ]);
  };

  const handleAnswerClick = async (optionIndex) => {
    if (selectedOption !== null || submittingAnswer || !quizQuestions[currentQuestionIndex]) return;

    setSelectedOption(optionIndex);
    setSubmittingAnswer(true);

    const currQ = quizQuestions[currentQuestionIndex];

    try {
      const res = await cultureService.submitQuizAnswer({
        festival: selectedFestival?.id || 'pongal',
        question_id: currQ.id,
        selected_index: optionIndex,
        language: currentLanguage
      });

      setSubmittedResult(res);

      if (res.is_correct) {
        setQuizScore((prev) => prev + 1);
        setQuizStreak((prev) => prev + 1);
        triggerCelebration();
      } else {
        setQuizStreak(0);
      }

      if (res.new_stamp_earned) {
        triggerCelebration();
      }
      refreshUser();
    } catch (err) {
      console.error('Error submitting quiz answer:', err);
    } finally {
      setSubmittingAnswer(false);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex + 1 < quizQuestions.length) {
      setCurrentQuestionIndex((prev) => prev + 1);
      setSelectedOption(null);
      setSubmittedResult(null);
    } else {
      setQuizCompleted(true);
      triggerCelebration();
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || loadingChat) return;

    const userText = inputText.trim();
    setInputText('');

    const newHistory = [...messages, { role: 'user', content: userText }];
    setMessages(newHistory);
    setLoadingChat(true);

    try {
      const historyPayload = messages.map((m) => ({ role: m.role, content: m.content }));
      const res = await cultureService.sendCultureChat(userText, historyPayload, currentLanguage);

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.response,
          media: res.media,
          videos: res.videos
        }
      ]);
      setUserStamps(res.stamps || []);

      if (res.stamps && res.stamps.length > userStamps.length) {
        triggerCelebration();
      }
      refreshUser();
    } catch (err) {
      console.error('Culture chat send error:', err);
    } finally {
      setLoadingChat(false);
    }
  };

  const currentQ = quizQuestions[currentQuestionIndex];
  const progressPercent = quizQuestions.length > 0 
    ? Math.round(((currentQuestionIndex + (submittedResult ? 1 : 0)) / quizQuestions.length) * 100) 
    : 0;

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-amber-200/80 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-black text-amber-700 uppercase tracking-wider mb-1">
            <Link to="/" className="hover:underline flex items-center gap-1">
              <ArrowLeft className="w-3.5 h-3.5" /> Dashboard
            </Link>
            <span>•</span>
            <span>Module 3: Cultural Discovery & Gamification</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-amber-950 tracking-tight">
            🪔 {selectedFestival ? `${selectedFestival.name} (${selectedFestival.native_name})` : 'Cultural Odyssey'}
          </h1>
          <p className="text-sm font-medium text-stone-600">
            Watch animated festival video stories, take the 10-question quiz, and unlock Cultural Stamps!
          </p>
        </div>

        <Link
          to="/progress"
          className="inline-flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-purple-100 to-amber-100 hover:from-purple-200 hover:to-amber-200 border border-purple-300 rounded-full text-purple-950 text-xs font-bold self-start sm:self-auto shadow-sm transition-all"
        >
          <Award className="w-4 h-4 text-purple-700" />
          <span>Cultural Passport ({user?.stamps?.length || userStamps.length || 0} Stamps)</span>
        </Link>
      </div>

      {/* Festival Selector Buttons */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="block text-xs font-bold text-stone-600 uppercase tracking-wider">
            Select a Festival:
          </label>
          <span className="text-xs font-semibold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full">
            {currentLanguage} Culture
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {festivals.map((fest) => (
            <button
              key={fest.id}
              onClick={() => handleSelectFestival(fest)}
              className={`p-3 rounded-2xl border-2 text-left transition-all flex items-start gap-3 select-none ${
                selectedFestival?.id === fest.id
                  ? 'bg-amber-100/90 border-amber-500 shadow-md scale-[1.02] ring-2 ring-amber-400/50'
                  : 'bg-white border-amber-200 hover:border-amber-400'
              }`}
            >
              <span className="text-3xl p-1 rounded-xl bg-amber-50 shrink-0">
                {fest.icon}
              </span>
              <div className="min-w-0 flex-1">
                <h4 className="font-extrabold text-sm text-stone-900 leading-tight truncate">
                  {fest.name}
                </h4>
                <span className="text-xs font-bold text-amber-800 block mt-0.5 truncate">
                  {fest.native_name}
                </span>
                <span className="inline-flex items-center gap-1 text-[10px] font-bold text-purple-700 mt-1">
                  <Trophy className="w-3 h-3 text-amber-600" /> 10 Quizzes
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Tab Navigation: 1. Video Stories | 2. Quiz Arena | 3. Folklore Chat */}
      <div className="flex items-center gap-2 border-b border-amber-200 pb-1">
        <button
          onClick={() => setActiveTab('video')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl text-xs sm:text-sm font-extrabold transition-all ${
            activeTab === 'video'
              ? 'bg-red-600 text-white shadow-md'
              : 'bg-white text-stone-700 border border-amber-200 hover:bg-amber-50'
          }`}
        >
          <Youtube className="w-4 h-4" />
          <span>🎬 Watch Video Stories</span>
          <span className="px-2 py-0.5 bg-red-700/60 rounded-full text-[10px]">{festivalVideos.length} Videos</span>
        </button>

        <button
          onClick={() => setActiveTab('quiz')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl text-xs sm:text-sm font-extrabold transition-all ${
            activeTab === 'quiz'
              ? 'bg-amber-500 text-white shadow-md'
              : 'bg-white text-stone-700 border border-amber-200 hover:bg-amber-50'
          }`}
        >
          <Trophy className="w-4 h-4" />
          <span>🏆 10-Question Quiz Arena</span>
          <span className="px-2 py-0.5 bg-amber-600/60 rounded-full text-[10px]">+10 Pts / Q</span>
        </button>

        <button
          onClick={() => setActiveTab('story')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl text-xs sm:text-sm font-extrabold transition-all ${
            activeTab === 'story'
              ? 'bg-amber-700 text-white shadow-md'
              : 'bg-white text-stone-700 border border-amber-200 hover:bg-amber-50'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          <span>👵 Ammachi's Folklore Chat</span>
        </button>
      </div>

      {/* TAB 1: WATCH VIDEO STORIES & THEATER */}
      {activeTab === 'video' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <div className="lg:col-span-8 bg-white border-2 border-amber-200 rounded-3xl p-5 sm:p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-amber-100 pb-3">
              <div className="flex items-center gap-2">
                <span className="p-2 rounded-xl bg-red-100 text-red-600">
                  <Youtube className="w-5 h-5" />
                </span>
                <div>
                  <h3 className="font-black text-stone-900 text-base">
                    {selectedFestival ? `${selectedFestival.name} Video Stories` : 'Festival Videos'}
                  </h3>
                  <p className="text-xs text-stone-500">
                    Watch animated stories and traditions in {currentLanguage}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setActiveTab('quiz')}
                className="btn-primary text-xs px-4 py-2 flex items-center gap-1.5"
              >
                <Trophy className="w-3.5 h-3.5" />
                <span>Take Quiz on this Video</span>
              </button>
            </div>

            {/* Video Player Embed */}
            {activeVideo ? (
              <div className="space-y-3">
                <div className="relative aspect-video w-full rounded-2xl overflow-hidden bg-black shadow-inner border border-stone-200">
                  <iframe
                    src={`${activeVideo.embed_url}?autoplay=0&rel=0&modestbranding=1`}
                    title={activeVideo.title}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                    className="w-full h-full border-0"
                  />
                </div>

                <div>
                  <h4 className="font-bold text-sm sm:text-base text-stone-900 leading-snug">
                    {activeVideo.title}
                  </h4>
                  {activeVideo.description && (
                    <p className="text-xs text-stone-600 mt-1 line-clamp-2">
                      {activeVideo.description}
                    </p>
                  )}
                  {activeVideo.channel_title && (
                    <span className="inline-block text-[11px] font-semibold text-amber-800 bg-amber-50 px-2.5 py-0.5 rounded-md mt-1.5">
                      Channel: {activeVideo.channel_title}
                    </span>
                  )}
                </div>
              </div>
            ) : loadingVideos ? (
              <div className="py-16 flex flex-col items-center justify-center space-y-2">
                <RefreshCw className="w-6 h-6 animate-spin text-red-600" />
                <p className="text-xs font-bold text-stone-600">Loading festival videos...</p>
              </div>
            ) : null}
          </div>

          {/* Video Playlist Sidebar */}
          <div className="lg:col-span-4 space-y-4">
            <div className="bg-white border-2 border-amber-200 rounded-3xl p-4 sm:p-5 shadow-sm space-y-3">
              <h4 className="font-black text-stone-900 text-sm uppercase tracking-wider">
                Playlist for {selectedFestival?.name}
              </h4>

              <div className="space-y-2">
                {festivalVideos.map((vid, idx) => (
                  <button
                    key={idx}
                    onClick={() => setActiveVideo(vid)}
                    className={`w-full p-2.5 rounded-2xl border text-left transition-all flex items-center gap-3 ${
                      activeVideo?.video_id === vid.video_id
                        ? 'bg-red-50 border-red-400 ring-2 ring-red-400'
                        : 'bg-stone-50 border-stone-200 hover:border-amber-300 hover:bg-white'
                    }`}
                  >
                    <div className="relative w-20 h-14 shrink-0 rounded-xl overflow-hidden bg-stone-200">
                      {vid.thumbnail ? (
                        <img src={vid.thumbnail} alt="" className="w-full h-full object-cover" />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center bg-stone-300">
                          <Play className="w-4 h-4 text-stone-600" />
                        </div>
                      )}
                      <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                        <Play className="w-4 h-4 text-white fill-white" />
                      </div>
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-xs font-bold text-stone-900 leading-tight line-clamp-2">
                        {vid.title}
                      </p>
                      <span className="text-[10px] text-stone-500 block mt-1">
                        {vid.channel_title}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Quick Challenge Promo */}
            <div className="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-200 rounded-3xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold text-amber-900">
                <Trophy className="w-4 h-4 text-amber-600" />
                <span>Ready for the Quiz?</span>
              </div>
              <p className="text-xs text-stone-700 leading-relaxed">
                Test your knowledge of the video story with 10 questions and earn +100 points!
              </p>
              <button
                onClick={() => setActiveTab('quiz')}
                className="btn-primary text-xs w-full py-2.5"
              >
                <span>Start 10-Question Quiz Now</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: INTERACTIVE GAMIFIED QUIZ ARENA */}
      {activeTab === 'quiz' && (
        <div className="space-y-6">
          <div className="bg-white border-2 border-amber-200 rounded-3xl p-5 sm:p-8 shadow-sm space-y-6">
            
            {/* Quiz Header & Gamification Bar */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-amber-100 pb-4">
              <div className="flex items-center gap-3">
                <span className="p-2.5 rounded-2xl bg-amber-100 text-2xl">
                  {selectedFestival?.icon || '🏆'}
                </span>
                <div>
                  <h3 className="font-black text-stone-900 text-base sm:text-lg">
                    {selectedFestival?.name} Cultural Quiz
                  </h3>
                  <p className="text-xs text-stone-500">
                    Question {Math.min(currentQuestionIndex + 1, quizQuestions.length)} of {quizQuestions.length}
                  </p>
                </div>
              </div>

              {/* Score & Streak Badges */}
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-orange-50 border border-orange-200 rounded-xl text-orange-800 text-xs font-black">
                  <Flame className="w-4 h-4 text-orange-600 animate-pulse" />
                  <span>Streak: {quizStreak}x</span>
                </div>
                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-purple-50 border border-purple-200 rounded-xl text-purple-900 text-xs font-black">
                  <Trophy className="w-4 h-4 text-purple-700" />
                  <span>Score: {quizScore} / {quizQuestions.length}</span>
                </div>
              </div>
            </div>

            {/* Animated Progress Bar */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs font-bold text-stone-500">
                <span>Quiz Progress</span>
                <span>{progressPercent}% Complete</span>
              </div>
              <div className="w-full bg-amber-100 rounded-full h-3 overflow-hidden p-0.5">
                <div 
                  className="bg-gradient-to-r from-amber-500 to-orange-500 h-full rounded-full transition-all duration-500 shadow-sm"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>

            {/* Quiz Body */}
            {loadingQuiz ? (
              <div className="py-16 flex flex-col items-center justify-center space-y-3">
                <RefreshCw className="w-8 h-8 animate-spin text-amber-600" />
                <p className="text-sm font-bold text-stone-700">Ammachi is gathering 10 festive quiz questions...</p>
              </div>
            ) : quizCompleted ? (
              /* Quiz Completion Celebration Card */
              <div className="py-10 flex flex-col items-center justify-center text-center space-y-5 bg-gradient-to-b from-amber-50 to-orange-50 rounded-3xl p-6 border-2 border-amber-300">
                <span className="text-6xl animate-bounce">🏆✨🎉</span>
                <div className="space-y-1">
                  <h3 className="text-2xl sm:text-3xl font-black text-amber-950">
                    Sabash, Kanna! Quiz Completed!
                  </h3>
                  <p className="text-sm font-medium text-stone-700 max-w-md">
                    You answered <strong>{quizScore} out of {quizQuestions.length}</strong> questions correctly and unlocked cultural knowledge!
                  </p>
                </div>

                <div className="p-4 bg-white rounded-2xl border-2 border-amber-300 shadow-sm flex items-center gap-4">
                  <span className="text-4xl">{selectedFestival?.icon}</span>
                  <div className="text-left">
                    <span className="text-[10px] font-bold text-purple-700 uppercase tracking-wider block">Cultural Passport Stamp</span>
                    <h4 className="font-extrabold text-stone-900 text-base">{selectedFestival?.name} Cultural Master</h4>
                    <span className="text-xs font-bold text-emerald-700">✅ Unlocked in Profile</span>
                  </div>
                </div>

                <div className="flex items-center gap-3 pt-2">
                  <button
                    onClick={() => loadQuiz(selectedFestival?.id || 'pongal')}
                    className="flex items-center gap-2 px-5 py-3 bg-white border border-amber-300 rounded-2xl font-bold text-xs sm:text-sm text-stone-800 hover:bg-amber-100 transition-all"
                  >
                    <RotateCcw className="w-4 h-4" />
                    <span>Retake Quiz</span>
                  </button>
                  <button
                    onClick={() => setActiveTab('video')}
                    className="btn-primary px-6 py-3 text-xs sm:text-sm flex items-center gap-2"
                  >
                    <Youtube className="w-4 h-4" />
                    <span>Watch {selectedFestival?.name} Video</span>
                  </button>
                </div>
              </div>
            ) : currentQ ? (
              /* Active Question Card */
              <div className="space-y-6">
                <div className="space-y-2">
                  <span className="inline-block px-3 py-1 bg-amber-100 text-amber-900 rounded-full text-xs font-extrabold uppercase">
                    Question {currentQuestionIndex + 1}
                  </span>
                  <h3 className="text-lg sm:text-xl font-black text-stone-900 leading-snug">
                    {currentQ.question}
                  </h3>
                </div>

                {/* 4 Interactive Option Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                  {currentQ.options.map((opt, idx) => {
                    const isSelected = selectedOption === idx;
                    const isCorrectAnswer = submittedResult && idx === submittedResult.correct_index;
                    const isWrongSelection = submittedResult && isSelected && !submittedResult.is_correct;

                    let cardStyle = 'bg-stone-50 border-stone-200 hover:border-amber-400 hover:bg-amber-50/50';

                    if (submittedResult) {
                      if (isCorrectAnswer) {
                        cardStyle = 'bg-emerald-50 border-emerald-500 ring-2 ring-emerald-400 text-emerald-950 font-bold';
                      } else if (isWrongSelection) {
                        cardStyle = 'bg-rose-50 border-rose-400 ring-2 ring-rose-300 text-rose-950';
                      } else {
                        cardStyle = 'opacity-60 bg-stone-50 border-stone-200';
                      }
                    } else if (isSelected) {
                      cardStyle = 'bg-amber-100 border-amber-500 ring-2 ring-amber-400';
                    }

                    return (
                      <button
                        key={idx}
                        onClick={() => handleAnswerClick(idx)}
                        disabled={selectedOption !== null || submittingAnswer}
                        className={`p-4 rounded-2xl border-2 text-left transition-all flex items-center justify-between gap-3 text-sm sm:text-base font-semibold select-none ${cardStyle}`}
                      >
                        <div className="flex items-center gap-3">
                          <span className="w-7 h-7 rounded-full bg-white border border-stone-300 flex items-center justify-center text-xs font-black text-stone-700 shrink-0">
                            {String.fromCharCode(65 + idx)}
                          </span>
                          <span>{opt}</span>
                        </div>

                        {submittedResult && isCorrectAnswer && (
                          <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
                        )}
                        {submittedResult && isWrongSelection && (
                          <X className="w-5 h-5 text-rose-600 shrink-0" />
                        )}
                      </button>
                    );
                  })}
                </div>

                {/* Grandmother Explanation Card */}
                {submittedResult && (
                  <div className={`p-4 sm:p-5 rounded-2xl border-2 space-y-3 animate-in fade-in duration-200 ${
                    submittedResult.is_correct 
                      ? 'bg-emerald-50 border-emerald-200 text-emerald-950'
                      : 'bg-amber-50 border-amber-200 text-amber-950'
                  }`}>
                    <div className="flex items-start gap-3">
                      <AmmachiMascot size="xs" className="shrink-0" />
                      <div className="space-y-1">
                        <h4 className="font-black text-sm">
                          {submittedResult.is_correct ? '🎉 Sabash Kanna! That is Correct! (+10 Points)' : '💡 Ammachi\'s Explanation:'}
                        </h4>
                        <p className="text-xs sm:text-sm leading-relaxed">
                          {submittedResult.explanation}
                        </p>
                      </div>
                    </div>

                    <div className="flex justify-end pt-1">
                      <button
                        onClick={handleNextQuestion}
                        className="btn-primary text-xs sm:text-sm px-6 py-2.5 flex items-center gap-2"
                      >
                        <span>{currentQuestionIndex + 1 < quizQuestions.length ? 'Next Question' : 'Complete Quiz'}</span>
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : null}
          </div>
        </div>
      )}

      {/* TAB 3: AMMACHI'S FOLKLORE CHAT */}
      {activeTab === 'story' && (
        <div className="bg-white border-2 border-amber-200 rounded-3xl p-5 sm:p-6 shadow-sm flex flex-col justify-between min-h-[500px]">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-amber-100 pb-3 mb-3">
            <div className="flex items-center gap-2">
              <AmmachiMascot size="xs" />
              <div>
                <h3 className="font-black text-stone-900 text-sm sm:text-base">
                  Ammachi's Storytelling Corner
                </h3>
                <p className="text-xs text-stone-500">
                  Ask Ammachi anything about {selectedFestival?.name} traditions
                </p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="space-y-3.5 max-h-[380px] overflow-y-auto pr-1 mb-3">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex gap-2.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'assistant' && (
                  <AmmachiMascot size="xs" className="shrink-0 self-start" />
                )}

                <div
                  className={`max-w-[85%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-amber-500 text-white rounded-tr-none shadow-sm font-medium'
                      : 'bg-amber-50 border border-amber-200 text-stone-800 rounded-tl-none shadow-sm'
                  }`}
                >
                  {/* Clean Formatted Text: Bolds keywords & Renders Real Bullet Points */}
                  <div className="space-y-2">
                    {msg.content.split('\n').map((line, lIdx) => {
                      const trimmed = line.trim();
                      if (!trimmed) return null;

                      const isBullet = trimmed.startsWith('•') || trimmed.startsWith('* ') || trimmed.startsWith('- ') || /^\d+\.\s/.test(trimmed);
                      let cleanLine = trimmed;
                      if (trimmed.startsWith('* ') || trimmed.startsWith('- ')) {
                        cleanLine = trimmed.substring(2).trim();
                      } else if (trimmed.startsWith('•')) {
                        cleanLine = trimmed.substring(1).trim();
                      }

                      // Parse bold segments like **keyword**
                      const renderLineWithBolds = (textStr) => {
                        const parts = textStr.split(/(\*\*[^*]+\*\*)/g);
                        return parts.map((part, pIdx) => {
                          if (part.startsWith('**') && part.endsWith('**')) {
                            const inner = part.slice(2, -2);
                            return (
                              <strong key={pIdx} className="font-extrabold text-amber-950">
                                {inner}
                              </strong>
                            );
                          }
                          // Remove any stray single asterisks
                          const stripped = part.replace(/\*/g, '');
                          return <span key={pIdx}>{stripped}</span>;
                        });
                      };

                      if (isBullet) {
                        return (
                          <div key={lIdx} className="flex items-start gap-2 pl-1 py-0.5">
                            <span className="text-amber-600 font-black text-sm leading-none shrink-0 mt-0.5">•</span>
                            <div className="flex-1 leading-relaxed text-stone-800">
                              {renderLineWithBolds(cleanLine)}
                            </div>
                          </div>
                        );
                      }

                      return (
                        <p key={lIdx} className="leading-relaxed">
                          {renderLineWithBolds(cleanLine)}
                        </p>
                      );
                    })}
                  </div>

                  {/* Attached Video Story Recommendations */}
                  {msg.videos && msg.videos.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-amber-200/60">
                      <button
                        onClick={() => {
                          setActiveVideo(msg.videos[0]);
                          setActiveTab('video');
                        }}
                        className="inline-flex items-center gap-1.5 text-xs font-bold text-red-700 hover:text-red-800 bg-red-50 hover:bg-red-100 border border-red-200 px-3 py-1.5 rounded-xl transition-all"
                      >
                        <Youtube className="w-3.5 h-3.5 text-red-600" />
                        <span>Watch Video: {msg.videos[0].title}</span>
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loadingChat && (
              <div className="flex items-center gap-2 text-stone-500 text-xs font-bold py-1">
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-amber-600" />
                <span>Ammachi is gathering folklore stories...</span>
              </div>
            )}
          </div>

          {/* Input Bar */}
          <form onSubmit={handleSendMessage} className="flex gap-2 pt-2.5 border-t border-amber-100">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask Ammachi a question about this festival..."
              className="flex-1 px-3.5 py-2.5 bg-amber-50/60 border border-amber-200 rounded-2xl text-stone-800 placeholder-stone-400 font-medium focus:outline-none focus:ring-2 focus:ring-amber-400 focus:bg-white text-xs sm:text-sm"
            />
            <button
              type="submit"
              disabled={loadingChat || !inputText.trim()}
              className="btn-primary px-5 py-2.5 text-xs sm:text-sm"
            >
              <Send className="w-4 h-4" />
              <span className="hidden sm:inline">Send</span>
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
