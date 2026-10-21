import React, { useEffect, useState } from 'react';
import { Flame, Gem, Heart, Zap, Trophy } from 'lucide-react';
import { learnService } from '../../services/learnService';

/**
 * Duolingo-style stat bar: daily-XP ring, streak, gems, hearts (+ league chip).
 * Fetches /learn/hud; pass `onChange` consumers or use let-point helpers elsewhere.
 */
export const LearnHud = ({ compact = false, refreshKey = 0 }) => {
  const [hud, setHud] = useState(null);
  const [tick, setTick] = useState(0);

  const refresh = () => setTick((t) => t + 1);

  useEffect(() => {
    let alive = true;
    learnService.getHud()
      .then((data) => { if (alive) setHud(data); })
      .catch(() => { if (alive) setHud(null); });
    return () => { alive = false; };
  }, [refreshKey, tick]);

  // Refresh when lesson completes / shop purchases happen / tab becomes visible again
  useEffect(() => {
    window.addEventListener('ammachi-hud-refresh', refresh);
    document.addEventListener('visibilitychange', refresh);
    return () => {
      window.removeEventListener('ammachi-hud-refresh', refresh);
      document.removeEventListener('visibilitychange', refresh);
    };
  }, []);

  if (!hud) return null;

  const goalPct = Math.min(100, Math.round((hud.xp_today / Math.max(1, hud.daily_goal)) * 100));

  return (
    <div className={`flex items-center justify-end gap-2 sm:gap-3 ${compact ? 'text-xs' : 'text-sm'}`}>
      {/* Daily goal ring */}
      <div
        className="flex items-center gap-1 font-black text-blue-700"
        title={`Daily goal: ${hud.xp_today}/${hud.daily_goal} XP`}
      >
        <Zap className={`w-4 h-4 ${hud.daily_goal_met ? 'fill-amber-400 text-amber-400' : 'text-blue-500'}`} />
        <span>{hud.xp_today}</span>
        <span className="text-stone-400 font-bold">/~{hud.daily_goal}</span>
        <span className="sr-only">{goalPct}% of daily goal</span>
      </div>

      {/* Streak */}
      <div className="flex items-center gap-1 font-black text-orange-600" title={`${hud.streak} day streak`}>
        <Flame className={`w-4 h-4 ${hud.streak > 0 ? 'fill-orange-500 text-orange-500' : 'text-stone-400'}`} />
        <span>{hud.streak}</span>
      </div>

      {/* Gems */}
      <div className="flex items-center gap-1 font-black text-cyan-600" title={`${hud.gems} gems`}>
        <Gem className="w-4 h-4 fill-cyan-500 text-cyan-500" />
        <span>{hud.gems}</span>
      </div>

      {/* Hearts */}
      <div className="flex items-center gap-1 font-black text-rose-600" title={`${hud.hearts}/${hud.hearts_max} hearts`}>
        <Heart className={`w-4 h-4 ${hud.hearts > 0 ? 'fill-rose-500 text-rose-500' : 'text-stone-300'}`} />
        <span>{hud.hearts}</span>
      </div>

      {/* League chip */}
      <div
        className="hidden sm:inline-flex items-center gap-1 rounded-full bg-purple-50 border border-purple-200 px-2.5 py-0.5 font-bold text-purple-700"
        title={`Current league: ${hud.league}`}
      >
        <Trophy className="w-3.5 h-3.5" />
        <span>{hud.league}</span>
      </div>
    </div>
  );
};
