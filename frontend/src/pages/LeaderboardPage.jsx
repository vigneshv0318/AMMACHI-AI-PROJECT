import React, { useEffect, useState } from 'react';
import { Trophy, ChevronUp, ChevronDown, Crown } from 'lucide-react';
import { learnService } from '../services/learnService';
import { AmmachiMascot } from '../components/common/AmmachiMascot';

export const LeaderboardPage = () => {
  const [board, setBoard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    learnService.getLeaderboard()
      .then((data) => alive && setBoard(data))
      .catch(() => {})
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <AmmachiMascot size="lg" speaking />
        <p className="font-bold text-amber-900">Counting the week's XP…</p>
      </div>
    );
  }

  const advances = board?.advances || 3;
  const entries = board?.entries || [];

  return (
    <div className="max-w-3xl mx-auto pb-16">
      <div className="flex items-center gap-3 mb-2">
        <h1 className="text-2xl sm:text-3xl font-black text-amber-900 tracking-tight flex-1">Leaderboard</h1>
      </div>

      {/* League banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-purple-500 to-indigo-500 p-5 border-2 border-purple-300/60 shadow-md shadow-purple-500/20 text-white">
        <span aria-hidden className="pointer-events-none absolute -top-8 -right-8 w-32 h-32 rounded-full bg-white/15" />
        <div className="flex items-center gap-3">
          <Crown className="w-8 h-8 fill-amber-300 text-amber-300" />
          <div className="flex-1">
            <h2 className="text-2xl font-black tracking-tight">{board?.league || 'Bronze'} League</h2>
            <p className="text-sm font-semibold text-white/85">
              Top {advances} advance to the next league · {board?.days_left ?? 7} days left
            </p>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-white rounded-3xl border-2 border-amber-200/80 shadow-sm divide-y divide-amber-100 overflow-hidden">
        {entries.length === 0 && (
          <p className="p-6 text-center font-bold text-stone-500">
            No XP earned this week yet — be the first to shine! ✨
          </p>
        )}
        {entries.map((e) => {
          const inPromotion = e.rank <= advances;
          const entry = (
            <div
              className={`flex items-center gap-3 px-4 py-3.5 ${e.is_current_user ? 'bg-amber-50' : ''} ${
                inPromotion ? '' : 'bg-stone-50'
              }`}
            >
              <span className={`w-8 text-right font-black text-lg tabular-nums ${inPromotion ? 'text-purple-600' : 'text-rose-400'}`}>
                {e.rank}
              </span>
              <AmmachiMascot size="xs" />
              <div className="flex-1 min-w-0">
                <p className="font-bold text-stone-800 truncate">
                  {e.username}
                  {e.is_current_user && <span className="ml-2 text-xs font-black text-amber-700">(you)</span>}
                </p>
              </div>
              <span className="font-black text-amber-700 tabular-nums">{e.xp} <span className="text-xs text-stone-400">XP</span></span>
            </div>
          );
          return e.rank === entries.length && !inPromotion ? null : (
            <React.Fragment key={e.rank}>
              {e.rank === advances + 1 && (
                <div className="px-4 py-1.5 bg-stone-100 text-xs font-black text-stone-500 uppercase tracking-wider flex items-center gap-1">
                  <ChevronDown className="w-3.5 h-3.5 text-rose-500" /> Demotion zone
                  <span className="flex-1" />
                  <ChevronUp className="w-3.5 h-3.5 text-purple-600" />
                  <span>Promotion zone</span>
                </div>
              )}
              {entry}
            </React.Fragment>
          );
        })}
      </div>

      <p className="mt-4 text-center text-sm font-semibold text-stone-500">
        Earn XP by finishing lessons to climb the {board?.league || 'Bronze'} League, kanna! 🏆
      </p>
    </div>
  );
};
