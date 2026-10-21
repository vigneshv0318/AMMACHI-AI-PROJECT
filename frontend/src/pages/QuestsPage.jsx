import React, { useEffect, useState } from 'react';
import { Zap, BookOpen, Target, Gem, Check } from 'lucide-react';
import { learnService } from '../services/learnService';
import { AmmachiMascot } from '../components/common/AmmachiMascot';

const QUEST_ICONS = {
  earn_xp: <Zap className="w-6 h-6 text-amber-500" />,
  finish_lessons: <BookOpen className="w-6 h-6 text-sky-500" />,
  correct_answers: <Target className="w-6 h-6 text-emerald-500" />,
};

export const QuestsPage = () => {
  const [hud, setHud] = useState(null);
  const [loading, setLoading] = useState(true);
  const [claimMsg, setClaimMsg] = useState(null);

  const load = () => {
    learnService.getHud()
      .then(setHud)
      .catch(() => {})
      .finally(() => setLoading(false));
  };
  useEffect(load, []);

  const claim = async (questType) => {
    try {
      const resp = await learnService.claimQuest(questType);
      setClaimMsg(`${resp.reward_gems} gems claimed! 💎`);
      setTimeout(() => setClaimMsg(null), 2400);
      window.dispatchEvent(new Event('ammachi-hud-refresh'));
      load();
    } catch (err) {
      const detail = err?.response?.data?.detail;
      alert(detail || 'Ammachi says: finish the quest first!');
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <AmmachiMascot size="lg" speaking />
        <p className="font-bold text-amber-900">Opening today's mission scroll…</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto pb-16">
      <div className="flex items-center gap-3 mb-5">
        <h1 className="text-2xl sm:text-3xl font-black text-amber-900 tracking-tight flex-1">Daily Quests</h1>
        <span className="inline-flex items-center gap-1 bg-cyan-50 border border-cyan-200 text-cyan-700 font-black px-3 py-1.5 rounded-full">
          <Gem className="w-4 h-4 fill-cyan-500 text-cyan-500" />
          {hud?.gems ?? 0}
        </span>
      </div>

      {claimMsg && (
        <div className="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-emerald-500 text-white px-4 py-2.5 rounded-2xl shadow-lg font-bold text-sm">
          {claimMsg}
        </div>
      )}

      <p className="font-bold text-stone-600 mb-4">
        Finish today's quests to collect gems. New quests every morning, kanna! 🌅
      </p>

      <div className="space-y-4">
        {(hud?.quests || []).map((q) => {
          const done = q.progress >= q.target && !q.claimed;
          const pct = Math.min(100, Math.round((q.progress / Math.max(1, q.target)) * 100));
          return (
            <div
              key={q.type}
              className={`rounded-3xl border-2 p-4 sm:p-5 transition-all ${
                q.claimed ? 'bg-stone-50 border-stone-200 opacity-70' : 'bg-white border-amber-200 shadow-sm'
              }`}
            >
              <div className="flex items-center gap-4">
                <span className={`flex items-center justify-center w-14 h-14 rounded-2xl shrink-0 ${q.claimed ? 'bg-stone-200' : 'bg-amber-100'}`}>
                  {q.claimed ? <Check className="w-7 h-7 text-stone-500" /> : QUEST_ICONS[q.type]}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="font-black text-stone-800">{q.title}</p>
                  <div className="mt-1.5 h-5 bg-stone-200/70 rounded-full overflow-hidden relative">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${q.claimed ? 'bg-stone-400' : 'bg-gradient-to-r from-amber-400 to-orange-400'}`}
                      style={{ width: `${pct}%` }}
                    />
                    <span className="absolute inset-0 flex items-center justify-center text-[11px] font-black text-stone-700">
                      {q.claimed ? 'Claimed! ✓' : `${q.progress} / ${q.target}`}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => claim(q.type)}
                  disabled={!done}
                  className={`shrink-0 flex items-center gap-1 px-4 py-2.5 rounded-2xl font-black text-sm border-b-4 transition-all ${
                    done
                      ? 'bg-amber-400 border-amber-600 text-amber-950 active:border-b-0 active:translate-y-1'
                      : 'bg-stone-200 border-stone-300 text-stone-400 cursor-not-allowed'
                  }`}
                >
                  <Gem className="w-4 h-4" />
                  {q.reward_gems}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
