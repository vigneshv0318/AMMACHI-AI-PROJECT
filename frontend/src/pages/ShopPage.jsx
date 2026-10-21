import React, { useEffect, useState } from 'react';
import { Gem, Heart, Shield, Target, ShoppingCart, Sparkles } from 'lucide-react';
import { learnService } from '../services/learnService';
import { AmmachiMascot } from '../components/common/AmmachiMascot';

const ITEM_ICONS = { hearts: <Heart />, streak_freeze: <Shield />, goal: <Target />, gems: <Gem /> };

export const ShopPage = () => {
  const [shop, setShop] = useState(null);
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState(null);
  const [busy, setBusy] = useState(null);

  const load = () => {
    learnService.getShop()
      .then(setShop)
      .catch(() => {})
      .finally(() => setLoading(false));
  };
  useEffect(load, []);

  const purchase = async (item) => {
    setBusy(item.id);
    try {
      const resp = await learnService.purchase(item.id);
      setMsg(`✨ ${resp.message}`);
      setTimeout(() => setMsg(null), 2600);
      window.dispatchEvent(new Event('ammachi-hud-refresh'));
      load();
    } catch (err) {
      const detail = err?.response?.data?.detail;
      alert(detail || 'Ammachi says: not enough gems, kanna!');
    } finally {
      setBusy(null);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <AmmachiMascot size="lg" speaking />
        <p className="font-bold text-amber-900">Setting up Ammachi's shop…</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto pb-16">
      <div className="flex items-center gap-3 mb-5">
        <h1 className="text-2xl sm:text-3xl font-black text-amber-900 tracking-tight flex-1">Shop</h1>
        <span className="inline-flex items-center gap-1 bg-cyan-50 border border-cyan-200 text-cyan-700 font-black px-3 py-1.5 rounded-full">
          <Gem className="w-4 h-4 fill-cyan-500 text-cyan-500" />
          {shop?.gems ?? 0}
        </span>
      </div>

      {msg && (
        <div className="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-emerald-500 text-white px-4 py-2.5 rounded-2xl shadow-lg font-bold text-sm">
          {msg}
        </div>
      )}

      {/* Hearts row (like Duolingo's shop hearts section) */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-rose-500 to-pink-500 p-5 border-2 border-rose-300/60 text-white shadow-md shadow-rose-500/20 mb-6">
        <div className="flex items-center gap-3">
          <Heart className="w-9 h-9 fill-white/90 text-white/90" />
          <div>
            <h2 className="text-xl font-black tracking-tight">Hearts</h2>
            <p className="text-sm font-semibold text-white/85">
              {shop?.hearts ?? 0} / {shop?.hearts_max ?? 5} hearts · Lose a heart for every wrong answer
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        {(shop?.items || []).map((item) => (
          <div
            key={item.id}
            className="flex items-center gap-4 bg-white rounded-3xl border-2 border-amber-200/80 shadow-sm p-4"
          >
            <span className="flex items-center justify-center w-12 h-12 rounded-2xl bg-amber-100 text-amber-700 shrink-0">
              {ITEM_ICONS[item.kind] || <Sparkles />}
            </span>
            <div className="flex-1 min-w-0">
              <p className="font-black text-stone-800">{item.title}</p>
              <p className="text-sm font-semibold text-stone-500">{item.description}</p>
            </div>
            {item.kind === 'goal' && shop?.daily_goal === item.extra?.goal ? (
              <span className="shrink-0 text-xs font-black text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-full">
                Active
              </span>
            ) : item.kind === 'streak_freeze' && shop?.streak_freezes > 0 ? (
              <span className="shrink-0 text-xs font-black text-cyan-600 bg-cyan-50 px-3 py-1.5 rounded-full">
                ×{shop.streak_freezes} equipped
              </span>
            ) : null}
            <button
              onClick={() => purchase(item)}
              disabled={busy === item.id || item.kind === 'streak_freeze' && shop?.streak_freezes > 1}
              className={`shrink-0 flex items-center gap-1.5 px-4 py-2.5 rounded-2xl font-black text-sm border-b-4 transition-all active:border-b-0 active:translate-y-1 ${
                item.cost === 0
                  ? 'bg-sky-500 border-sky-700 text-white hover:brightness-105'
                  : 'bg-amber-400 border-amber-600 text-amber-950 hover:brightness-105'
              } disabled:opacity-40`}
            >
              {item.cost === 0 ? (
                <>Set</>
              ) : (
                <><Gem className="w-4 h-4 fill-cyan-500 text-cyan-700" /> {item.cost}</>
              )}
            </button>
          </div>
        ))}
      </div>

      <p className="mt-5 text-center text-sm font-semibold text-stone-500">
        Gems are earned from perfect lessons and daily quests 💎
      </p>
    </div>
  );
};
