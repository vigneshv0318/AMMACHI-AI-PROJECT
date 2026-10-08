import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, PenLine, Mic, Sparkles, Award } from 'lucide-react';

export const BottomNav = () => {
  const navItems = [
    { to: '/', label: 'Home', icon: Home, end: true },
    { to: '/handwriting', label: 'Write', icon: PenLine },
    { to: '/speaking', label: 'Speak', icon: Mic },
    { to: '/culture', label: 'Culture', icon: Sparkles },
    { to: '/progress', label: 'Passport', icon: Award },
  ];

  return (
    <nav
      aria-label="Main"
      className="fixed bottom-0 inset-x-0 z-40 sm:hidden bg-white/95 backdrop-blur-md border-t border-amber-200/80 shadow-[0_-4px_20px_rgba(180,83,9,0.08)] pb-[env(safe-area-inset-bottom)]"
    >
      <div className="grid grid-cols-5 px-1">
        {navItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex flex-col items-center justify-center gap-0.5 h-16 select-none transition-colors ${
                isActive ? 'text-amber-700' : 'text-stone-500 active:text-stone-800'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <span
                  className={`flex items-center justify-center w-12 h-8 rounded-full transition-all ${
                    isActive ? 'bg-gradient-to-r from-amber-200 to-orange-200 shadow-sm' : ''
                  }`}
                >
                  <Icon className={`w-5 h-5 ${isActive ? 'stroke-[2.5]' : ''}`} />
                </span>
                <span className={`text-[11px] leading-none ${isActive ? 'font-extrabold' : 'font-semibold'}`}>{label}</span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
};
