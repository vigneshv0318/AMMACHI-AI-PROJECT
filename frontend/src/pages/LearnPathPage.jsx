import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Star, BookOpen, Dumbbell, Gift, Trophy, Lock, Check,
  Flame, Gem, Heart, Zap, ChevronLeft,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { learnService } from '../services/learnService';
import { AmmachiMascot } from '../components/common/AmmachiMascot';

const NODE_ICON = {
  lesson: Star,
  story: BookOpen,
  practice: Dumbbell,
  chest: Gift,
  unit_review: Trophy,
};

const NODE_LABEL = {
  lesson: 'Lesson',
  story: 'Story',
  practice: 'Practice',
  chest: 'Chest',
  unit_review: 'Unit Review',
};

// Zig-zag offsets like Duolingo's snaking path (px travel, fits ~360px screens)
const SNAKE = [0, 46, 88, 46, 0, -46, -88, -46];

export const LearnPathPage = () => {
  const { currentLanguage, activeLangMeta } = useLanguage();
  const navigate = useNavigate();
  const [path, setPath] = useState(null);
  const [loading, setLoading] = useState(true);
  const [preview, setPreview] = useState(null);      // node intro modal data
  const [previewLoading, setPreviewLoading] = useState(false);
  const [starting, setStarting] = useState(false);
  const [hudRefresh, setHudRefresh] = useState(0);
  const [chestMsg, setChestMsg] = useState(null);

  const loadPath = useCallback(async () => {
    setLoading(true);
    try {
      const data = await learnService.getPath(currentLanguage);
      setPath(data);
    } catch (err) {
      console.warn('Learn path load failed:', err);
    } finally {
      setLoading(false);
    }
  }, [currentLanguage]);

  useEffect(() => { loadPath(); }, [loadPath]);

  const flatNodes = useMemo(() => {
    if (!path) return [];
    return path.units.flatMap((u) => u.nodes);
  }, [path]);

  const openNode = async (node) => {
    if (node.node_type === 'chest') {
      setChestMsg(node.completed
        ? { text: 'You already opened this chest! 🎉', unlocked: true }
        : { text: 'This chest opens after the current lesson. Keep going, kanna!', unlocked: false });
      setTimeout(() => setChestMsg(null), 2600);
      return;
    }
    if (node.locked) return;
    setPreviewLoading(true);
    try {
      const data = await learnService.getNodePreview(node.id);
      setPreview({ node, data });
    } catch (err) {
      console.warn('Node preview failed:', err);
    } finally {
      setPreviewLoading(false);
    }
  };

  const startLesson = async () => {
    if (!preview) return;
    setStarting(true);
    try {
      const attempt = await learnService.startAttempt(preview.node.id);
      navigate('/learn/lesson', {
        state: {
          attemptId: attempt.attempt_id,
          exercises: attempt.exercises,
          nodeTitle: preview.data.title,
          nodeType: preview.node.node_type,
          hearts: attempt.hearts,
          heartsMax: attempt.hearts_max,
          xp: attempt.xp,
        },
      });
    } catch (err) {
      const detail = err?.response?.data?.detail;
      alert(detail || 'Aiyayo! Could not start the lesson.');
    } finally {
      setStarting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <AmmachiMascot size="lg" speaking />
        <p className="font-bold text-amber-900">Ammachi is preparing your path…</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto pb-16">
      {/* Header */}
      <div className="flex items-center gap-3 mb-5">
        <h1 className="text-2xl sm:text-3xl font-black text-amber-900 tracking-tight flex-1">
          Learning Path
          <span className="block text-sm font-bold text-amber-700/80">{activeLangMeta.nativeName} · {path?.units?.length || 0} units</span>
        </h1>
      </div>

      {/* Quick links to gamification hubs (Duolingo sidebar equivalents) */}
      <div className="grid grid-cols-3 gap-2 sm:gap-3 mb-7">
        {[
          { to: '/leaderboard', label: 'Leagues', emoji: '🏆', color: 'from-purple-400 to-indigo-400 border-purple-300' },
          { to: '/quests', label: 'Quests', emoji: '📜', color: 'from-amber-400 to-orange-400 border-amber-300' },
          { to: '/shop', label: 'Shop', emoji: '🛒', color: 'from-rose-400 to-pink-400 border-rose-300' },
        ].map((q) => (
          <button
            key={q.to}
            onClick={() => navigate(q.to)}
            className={`flex flex-col items-center gap-0.5 rounded-2xl bg-gradient-to-b ${q.color} border-2 border-b-4 px-2 py-2.5 text-white font-black shadow-sm active:border-b-2 active:translate-y-0.5 transition-all`}
          >
            <span className="text-lg leading-none">{q.emoji}</span>
            <span className="text-[11px] sm:text-sm">{q.label}</span>
          </button>
        ))}
      </div>

      {chestMsg && (
        <div className={`fixed top-20 left-1/2 -translate-x-1/2 z-50 px-4 py-2.5 rounded-2xl shadow-lg font-bold text-sm ${chestMsg.unlocked ? 'bg-emerald-500 text-white' : 'bg-stone-800 text-white'}`}>
          {chestMsg.text}
        </div>
      )}

      {(path?.units || []).map((unit) => (
        <section key={unit.id} className="mb-10">
          {/* Unit banner */}
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-sky-500 to-cyan-500 p-4 sm:p-5 shadow-md shadow-sky-500/20 border-2 border-sky-300/70">
            <span aria-hidden="true" className="pointer-events-none absolute -top-8 -right-8 w-32 h-32 rounded-full bg-white/15" />
            <h2 className="text-center text-white text-xs font-black uppercase tracking-[0.2em] opacity-90">
              Unit {unit.order}
            </h2>
            <p className="text-center text-white text-lg sm:text-2xl font-black tracking-tight">{unit.title}</p>
            {unit.description && (
              <p className="text-center text-white/85 text-xs sm:text-sm font-medium mt-0.5">{unit.description}</p>
            )}
            {/* progress mini-bar */}
            <div className="mx-auto mt-2.5 max-w-[220px] h-2.5 rounded-full bg-white/25 overflow-hidden">
              <div className="h-full rounded-full bg-amber-300 transition-all duration-500" style={{ width: `${unit.progress_pct}%` }} />
            </div>
          </div>

          {/* Node snake + scenery */}
          <div className="relative mt-6 flex flex-col items-center">
            <UnitScenery unitOrder={unit.order} />
            {unit.nodes.map((node, idx) => (
              <PathNode
                key={node.id}
                node={node}
                offset={SNAKE[idx % SNAKE.length]}
                delay={idx * 80}
                onClick={() => openNode(node)}
              />
            ))}
          </div>
        </section>
      ))}

      {/* Node intro modal */}
      {preview && (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/40 p-4" onClick={() => !starting && setPreview(null)}>
          <div
            className="w-full max-w-md bg-white rounded-3xl p-6 shadow-2xl border-2 border-amber-200"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start gap-4">
              <AmmachiMascot size="md" speaking />
              <div className="flex-1 min-w-0">
                <h3 className="text-xl font-black text-amber-900">
                  {NODE_LABEL[preview.node.node_type] || 'Lesson'}
                </h3>
                <p className="text-sm font-semibold text-stone-600">
                  {preview.data.title} · Lesson {Math.min(preview.data.lesson_no, preview.data.lesson_total)} of {preview.data.lesson_total}
                </p>
                <p className="mt-2 inline-flex items-center gap-1 text-sm font-black text-amber-700 bg-amber-100 rounded-full px-3 py-1">
                  <Zap className="w-4 h-4" /> +{preview.data.xp} XP
                </p>
              </div>
            </div>

            <button
              onClick={startLesson}
              disabled={starting}
              className="mt-5 w-full btn-primary disabled:opacity-60"
            >
              {starting ? 'Opening…' : `Start +${preview.data.xp} XP`}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const PathNode = ({ node, offset, delay = 0, onClick }) => {  const Icon = NODE_ICON[node.node_type] || Star;

  let style = 'bg-sky-400 border-sky-500 text-white shadow-[0_5px_0_0_rgba(2,132,199,1)] hover:brightness-105';
  let inner = null;

  if (node.completed) {
    style = 'bg-emerald-500 border-emerald-600 text-white shadow-[0_5px_0_0_rgba(5,150,105,1)] hover:brightness-105';
    inner = (
      <span className="relative">
        {node.node_type === 'lesson' || node.node_type === 'unit_review' ? (
          <span className="flex">
            {[...Array(3)].map((_, i) => (
              <Star key={i} className={`w-3.5 h-3.5 ${i < node.stars ? 'fill-amber-300 text-amber-300' : 'fill-white/30 text-white/30'} -ml-0.5`} />
            ))}
          </span>
        ) : (
          <Check className="w-4 h-4" strokeWidth={4} />
        )}
      </span>
    );
  } else if (node.locked) {
    style = 'bg-stone-300 border-stone-300 text-stone-400 shadow-[0_5px_0_0_rgba(168,162,158,1)] cursor-not-allowed';
  } else if (node.node_type === 'chest') {
    style = 'bg-amber-400 border-amber-500 text-white shadow-[0_5px_0_0_rgba(217,119,6,1)] hover:brightness-105';
  }

  return (
    <div className="relative" style={{ transform: `translateX(${offset}%)`, marginBottom: '18px' }}>
      {node.is_current && (
        <div className="absolute -top-9 left-1/2 -translate-x-1/2 z-10 start-bob">
          <div className="relative bg-white border-2 border-sky-400 text-sky-600 text-xs font-black px-3 py-1 rounded-xl shadow-md">
            START
            <span className="absolute bottom-[-7px] left-1/2 -translate-x-1/2 w-3 h-3 bg-white border-r-2 border-b-2 border-sky-400 rotate-45" />
          </div>
        </div>
      )}
      <button
        onClick={onClick}
        aria-label={`${NODE_LABEL[node.node_type] || 'Node'} node${node.is_current ? ' (start here)' : ''}`}
        className={`node-pop relative flex items-center justify-center w-[68px] h-[62px] rounded-[50%] border-2 active:translate-y-[3px] active:shadow-[0_2px_0_0_rgba(0,0,0,0.2)] transition-all ${style} ${
          node.is_current && !node.completed ? 'node-pulse' : ''
        }`}
        style={{ animationDelay: `${delay}ms` }}
      >
        {node.node_type !== 'lesson' && node.node_type !== 'unit_review' && !(node.completed) && (
          <Icon className={node.locked ? 'w-6 h-6 opacity-60' : 'w-6 h-6'} />
        )}
        {node.node_type !== 'lesson' && node.node_type !== 'unit_review' && node.completed && inner}
        {node.completed && (node.node_type === 'lesson' || node.node_type === 'unit_review') && inner}
        {!node.completed && (node.node_type === 'lesson' || node.node_type === 'unit_review') && (
          node.locked ? <Lock className="w-5 h-5" /> : <Icon className="w-6 h-6" />
        )}
        {node.completed && node.node_type === 'lesson' && <span className="sr-only">completed</span>}
      </button>
      {node.locked && <Lock className="absolute -bottom-1 -right-1 w-5 h-5 bg-stone-400 rounded-full p-0.5 text-white" />}
    </div>
  );
};

// Side scenery to fill the empty margins (desktop only). Alternates by unit.
const UnitScenery = ({ unitOrder }) => {
  const left = unitOrder % 2 === 1;
  const first = unitOrder === 1;
  return (
    <div aria-hidden="true" className="pointer-events-none absolute inset-0 hidden sm:block">
      {/* Ammachi cheering beside the path */}
      <div className={`absolute top-[14%] ${left ? 'left-[2%]' : 'right-[2%]'} flex flex-col items-center gap-1`}>
        <AmmachiMascot size="sm" className="floaty" speaking />
        <span className="rotate-[-4deg] text-[11px] font-black text-amber-800 bg-white/90 border-2 border-amber-300 rounded-xl px-2 py-1 shadow-sm text-center max-w-[130px] leading-tight">
          {first
            ? 'Vaa kanna! Your adventure starts here ✨'
            : unitOrder % 2 === 0
              ? 'Super! Keep climbing the path! 🌟'
              : 'Ammachi is so proud of you! 🪔'}
        </span>
      </div>

      {left ? (
        <>
          <span className="absolute top-[46%] right-[8%] text-4xl floaty-slow">🦜</span>
          <span className="absolute bottom-[8%] left-[6%] text-5xl floaty">🌳</span>
          <span className="absolute top-[60%] left-[14%] text-2xl floaty-slow">✨</span>
        </>
      ) : (
        <>
          <span className="absolute top-[44%] left-[8%] text-4xl floaty-slow">🌻</span>
          <span className="absolute bottom-[8%] right-[6%] text-5xl floaty">🪔</span>
          <span className="absolute top-[58%] right-[14%] text-2xl floaty-slow">✨</span>
        </>
      )}
      <span className={`absolute bottom-[2%] ${left ? 'right-[10%]' : 'left-[10%]'} text-6xl floaty-slow opacity-90`}>
        🌄
      </span>
    </div>
  );
};
