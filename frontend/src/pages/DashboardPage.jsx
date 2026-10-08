import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Edit3, Mic, Sparkles, Star, Flame, Award, ArrowRight, BookOpen, Compass, ChevronRight, Swords } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { userService } from '../services/userService';
import { AmmachiMascot } from '../components/common/AmmachiMascot';
import { SpeechBubble } from '../components/common/SpeechBubble';

export const DashboardPage = () => {
  const { user } = useAuth();
  const { currentLanguage, activeLangMeta } = useLanguage();
  const [failedIcons, setFailedIcons] = useState({});
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await userService.getProfile();
        setProfile(data);
      } catch (err) {
        console.warn('Profile fetch warning:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [currentLanguage]);

  const greetingName = user?.username || 'Kanna';
  const progressPercent = profile?.overall_progress || 0;
  const points = profile?.points ?? user?.points ?? 0;
  const streak = profile?.streak || 1;
  const badgesCount = profile?.badges_count || profile?.stamps?.length || 0;

  const modules = [

    {
      id: 'challenge',
      title: 'Ammachi Challenge',
      subtitle: 'Friend vs Friend',
      nativeTitle: currentLanguage === 'Tamil' ? 'போட்டி' : (currentLanguage === 'Telugu' ? 'పోటీ' : 'चुनौती'),
      description: 'Challenge a friend to a 5-minute AI language battle! Compete in real-time.',
      icon: Swords,
      emoji: '⚔️',
      imagePath: '/icons/challenge.svg',
      color: 'from-amber-500 to-orange-500',
      bgColor: 'bg-amber-50 border-amber-300',
      textColor: 'text-amber-900',
      link: '/challenge',
      score: profile?.challenge_score || 0,
      badgeText: 'Multiplayer + AI'
    },
    {
      id: 'voice',
      title: 'AI Voice Agent',
      subtitle: 'Speaking Studio',
      nativeTitle: currentLanguage === 'Tamil' ? 'பேச்சுப் பயிற்சி' : (currentLanguage === 'Telugu' ? 'సంభాషణ' : 'बातचीत'),
      description: 'Speak and practice with patient AI Ammachi. Learn native accents and conversational fluency.',
      icon: Mic,
      emoji: '🎤',
      imagePath: '/icons/voice.svg',
      color: 'from-emerald-500 to-teal-500',
      bgColor: 'bg-emerald-50 border-emerald-300',
      textColor: 'text-emerald-900',
      link: '/speaking',
      score: profile?.speaking_score || 0,
      badgeText: 'Deepgram + ElevenLabs'
    },
    {
      id: 'culture',
      title: 'Cultural Discovery',
      subtitle: 'Heritage & Gamification',
      nativeTitle: currentLanguage === 'Tamil' ? 'கலாச்சார பயணம்' : (currentLanguage === 'Telugu' ? 'సంస్కృతి' : 'संस्कృతి'),
      description: 'Explore Indian festivals, moral folktales, solve quiz challenges, and collect stamps.',
      icon: Sparkles,
      emoji: '🪔',
      imagePath: '/icons/culture.svg',
      color: 'from-purple-500 to-pink-500',
      bgColor: 'bg-purple-50 border-purple-300',
      textColor: 'text-purple-900',
      link: '/culture',
      score: profile?.culture_score || 0,
      badgeText: 'LangGraph + Badges'
    },
    {
      id: 'handwriting',
      title: 'Handwriting Practice',
      subtitle: 'Writing Notebook',
      nativeTitle: currentLanguage === 'Tamil' ? 'கையெழுத்து' : (currentLanguage === 'Telugu' ? 'దస్తూరి' : 'हस्तलेख'),
      description: 'Write letters on real paper, take a photo, and Ammachi will check them!',
      icon: Edit3,
      emoji: '✍️',
      imagePath: '/icons/handwriting.svg',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50 border-blue-300',
      textColor: 'text-blue-900',
      link: '/handwriting',
      score: profile?.handwriting_score || 0,
      badgeText: 'OCR Assessment'
    }
  ];

  return (
    <div className="space-y-6 sm:space-y-8 animate-in fade-in duration-200">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden bg-gradient-to-br from-amber-400 via-amber-300 to-orange-300 rounded-3xl p-5 sm:p-8 shadow-lg shadow-amber-500/15 border-2 border-amber-300/80 flex flex-col md:flex-row md:items-center justify-between gap-5 sm:gap-6">
        {/* soft decorative circles */}
        <span aria-hidden="true" className="pointer-events-none absolute -top-10 -right-10 w-40 h-40 rounded-full bg-white/20" />
        <span aria-hidden="true" className="pointer-events-none absolute -bottom-12 -left-8 w-32 h-32 rounded-full bg-orange-400/20" />

        <div className="relative flex items-center gap-4 sm:gap-6 min-w-0">
          <AmmachiMascot size="lg" className="ring-4 ring-white/70" />
          <div className="space-y-1.5 min-w-0">
            <div className="inline-flex max-w-full items-center px-3 py-1 rounded-full bg-white/70 text-amber-950 text-[11px] sm:text-xs font-black uppercase tracking-wider backdrop-blur-sm">
              <span className="truncate">{activeLangMeta.greeting}</span>
            </div>
            <h1 className="text-[22px] leading-tight sm:text-3xl font-black text-amber-950 tracking-tight break-words">
              {greetingName}, ready to learn {currentLanguage}?
            </h1>
            <p className="text-amber-900/90 text-sm sm:text-base font-medium max-w-lg hidden min-[400px]:block">
              Let's write letters, talk to Ammachi, and unlock festive cultural stamps today!
            </p>
          </div>
        </div>

        {/* Quick Progress Ring Card */}
        <div className="relative bg-white/85 backdrop-blur-sm rounded-2xl p-3.5 sm:p-5 flex items-center gap-3 sm:gap-4 shrink-0 shadow-sm border border-white/80 w-full md:w-auto justify-around">
          <div className="text-center">
            <div className="text-2xl font-black text-amber-900 flex items-center justify-center gap-1">
              <Star className="w-5 h-5 text-amber-500 fill-amber-400" />
              <span>{points}</span>
            </div>
            <span className="text-[11px] font-bold text-stone-600 uppercase tracking-wider">Points</span>
          </div>

          <div className="w-px h-8 bg-amber-200" />

          <div className="text-center">
            <div className="text-2xl font-black text-orange-600 flex items-center justify-center gap-1">
              <Flame className="w-5 h-5 text-orange-500 fill-orange-400" />
              <span>{streak}d</span>
            </div>
            <span className="text-[11px] font-bold text-stone-600 uppercase tracking-wider">Streak</span>
          </div>

          <div className="w-px h-8 bg-amber-200" />

          <div className="text-center">
            <div className="text-2xl font-black text-purple-700 flex items-center justify-center gap-1">
              <Award className="w-5 h-5 text-purple-600" />
              <span>{badgesCount}</span>
            </div>
            <span className="text-[11px] font-bold text-stone-600 uppercase tracking-wider">Stamps</span>
          </div>
        </div>
      </div>

      {/* Ammachi's Daily Advice Bubble */}
      <SpeechBubble
        title="Ammachi's Daily Wisdom"
        text={`Vanakkam Kanna! Consistency is the key to mastering your native language. Try spending 5 minutes writing a letter in your notebook, or practice saying a new phrase with me!`}
      />

      {/* Module Selection Section */}
      <div>
        <div className="flex items-end justify-between gap-3 mb-3 sm:mb-4">
          <h2 className="text-xl sm:text-2xl font-black text-stone-900 tracking-tight flex items-center gap-2">
            <Compass className="w-6 h-6 text-amber-600 shrink-0" />
            <span>Learning Modules</span>
          </h2>
          <span className="text-xs font-bold text-stone-500 uppercase tracking-wider hidden sm:block">
            Tap a module to start
          </span>
        </div>

        <div className="grid grid-cols-1 min-[480px]:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-5">
          {modules.map((mod) => (
            <Link
              key={mod.id}
              to={mod.link}
              className={`module-card ${mod.bgColor} p-4 sm:p-6 flex flex-col justify-between group active:scale-[0.98]`}
            >
              <div className="flex min-[480px]:flex-col gap-4 min-[480px]:gap-4">
                <div className="flex items-start justify-between shrink-0">
                  <div className="w-16 h-16 sm:w-[72px] sm:h-[72px] shrink-0 flex items-center justify-center transform group-hover:scale-105 group-hover:-rotate-3 transition-transform">
                    {mod.imagePath && !failedIcons[mod.id] ? (
                      <img
                        src={mod.imagePath}
                        alt=""
                        draggable="false"
                        onError={() => setFailedIcons((prev) => ({ ...prev, [mod.id]: true }))}
                        className="w-full h-full object-contain drop-shadow-md"
                      />
                    ) : (
                      <span className="text-4xl">{mod.emoji}</span>
                    )}
                  </div>
                  <span className="hidden min-[480px]:inline-block text-[10px] font-extrabold px-2 py-1 rounded-full bg-white/90 text-stone-700 shadow-sm text-center max-w-[96px] leading-tight flex-shrink-0">
                    {mod.badgeText}
                  </span>
                </div>

                <div className="min-w-0 space-y-1.5 min-[480px]:space-y-3">
                  <div>
                    <span className="text-[11px] sm:text-xs font-bold text-stone-500 uppercase tracking-wider block">
                      {mod.subtitle}
                    </span>
                    <h3 className={`text-lg sm:text-xl font-black ${mod.textColor} leading-tight mt-0.5 group-hover:text-amber-700 transition-colors`}>
                      {mod.title}
                    </h3>
                    <span className="text-sm font-bold text-amber-800/80 block mt-0.5">
                      {mod.nativeTitle}
                    </span>
                  </div>

                  <p className="text-[13px] sm:text-sm text-stone-600 font-medium leading-relaxed line-clamp-2 min-[480px]:line-clamp-none">
                    {mod.description}
                  </p>
                </div>
              </div>

              <div className="mt-3 sm:mt-6 pt-3 sm:pt-4 border-t border-stone-200/60 flex items-center justify-between">
                <span className="text-xs font-bold text-stone-500">
                  Mastery: <strong className="text-stone-800 font-black">{mod.score}%</strong>
                </span>
                <span className="inline-flex items-center gap-1 text-sm font-bold text-amber-700 group-hover:translate-x-1 transition-transform">
                  <span>Start</span>
                  <ChevronRight className="w-4 h-4" />
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};
