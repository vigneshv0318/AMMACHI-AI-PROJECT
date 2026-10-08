import React, { useEffect, useState } from 'react';
import { AmmachiMascot } from './AmmachiMascot';

export const LoadingScreen = ({ message = "Opening Ammachi's Classroom..." }) => {
  // The free backend sleeps when idle; after a few seconds, explain the wait
  const [slow, setSlow] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setSlow(true), 4000);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="min-h-screen min-h-[100dvh] flex flex-col items-center justify-center gap-5 bg-warmbg text-amber-900 px-6 text-center">
      <div className="relative">
        <span aria-hidden="true" className="absolute inset-0 rounded-full bg-amber-300/50 animate-ping" />
        <AmmachiMascot size="xl" className="relative animate-bounce-soft" />
      </div>
      <p className="text-lg font-black tracking-tight">{message}</p>
      <div className="flex gap-1.5" aria-hidden="true">
        {[0, 1, 2].map((i) => (
          <span key={i} className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-bounce" style={{ animationDelay: `${i * 150}ms` }} />
        ))}
      </div>
      {slow && (
        <p className="text-sm font-semibold text-stone-500 max-w-xs animate-in fade-in">
          Ammachi is waking up the classroom. The first visit can take up to a minute.
        </p>
      )}
    </div>
  );
};
