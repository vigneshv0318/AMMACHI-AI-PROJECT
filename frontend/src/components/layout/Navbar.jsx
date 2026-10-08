import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { Flame, Star, Globe, User, ChevronDown, Check } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { AmmachiMascot } from '../common/AmmachiMascot';

export const Navbar = () => {
  const { user } = useAuth();
  const { currentLanguage, setLanguage, languages, activeLangMeta } = useLanguage();
  const [langMenuOpen, setLangMenuOpen] = useState(false);
  const menuRef = useRef(null);

  // Close the language menu on outside tap or Escape
  useEffect(() => {
    if (!langMenuOpen) return;
    const onPointer = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) setLangMenuOpen(false);
    };
    const onKey = (e) => e.key === 'Escape' && setLangMenuOpen(false);
    document.addEventListener('pointerdown', onPointer);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('pointerdown', onPointer);
      document.removeEventListener('keydown', onKey);
    };
  }, [langMenuOpen]);

  return (
    <header className="sticky top-0 z-40 bg-warmbg/90 backdrop-blur-md border-b border-amber-200/70 px-3 sm:px-6 pt-safe">
      <div className="max-w-6xl mx-auto flex items-center justify-between gap-2 sm:gap-4 h-14 sm:h-[72px]">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-2 sm:gap-3 min-w-0 group">
          <AmmachiMascot size="xs" className="sm:hidden" />
          <AmmachiMascot size="sm" className="hidden sm:inline-flex" />
          <div className="flex flex-col min-w-0">
            <span className="text-lg leading-tight sm:text-2xl font-black text-amber-900 tracking-tight truncate group-hover:text-amber-600 transition-colors">
              <span className="min-[420px]:hidden">Ammachi</span>
              <span className="hidden min-[420px]:inline">Ammachi's Class</span>
            </span>
            <span className="text-[11px] sm:text-xs font-semibold text-amber-700/80 truncate hidden min-[420px]:block">
              {activeLangMeta.greeting}
            </span>
          </div>
        </Link>

        {/* Right side */}
        <div className="flex items-center gap-1.5 sm:gap-3 shrink-0">
          {/* Language selector */}
          <div className="relative" ref={menuRef}>
            <button
              onClick={() => setLangMenuOpen((v) => !v)}
              type="button"
              aria-haspopup="listbox"
              aria-expanded={langMenuOpen}
              aria-label={`Language: ${activeLangMeta.name || currentLanguage}`}
              className="inline-flex items-center gap-1 h-9 px-2.5 sm:px-3 rounded-full bg-amber-100/80 hover:bg-amber-200 active:scale-95 text-amber-900 font-bold text-xs sm:text-sm border border-amber-300 shadow-sm transition-all"
            >
              <Globe className="w-3.5 h-3.5 text-amber-700 hidden sm:block" />
              <span className="max-w-[64px] sm:max-w-none truncate">{activeLangMeta.nativeName}</span>
              <ChevronDown className={`w-3 h-3 text-amber-700 transition-transform ${langMenuOpen ? 'rotate-180' : ''}`} />
            </button>

            {langMenuOpen && (
              <div
                role="listbox"
                className="absolute right-0 mt-2 w-52 max-w-[calc(100vw-1.5rem)] bg-white border-2 border-amber-200 rounded-2xl shadow-xl py-2 z-50 animate-in fade-in zoom-in-95 duration-150"
              >
                <div className="px-4 py-1.5 text-[11px] font-black text-stone-500 uppercase tracking-wider">
                  Select Language
                </div>
                {languages.map((lang) => (
                  <button
                    key={lang.id}
                    role="option"
                    aria-selected={currentLanguage === lang.id}
                    onClick={() => {
                      setLanguage(lang.id);
                      setLangMenuOpen(false);
                    }}
                    className={`w-full text-left px-4 py-3 text-sm flex items-center justify-between gap-3 hover:bg-amber-50 active:bg-amber-100 transition-colors ${
                      currentLanguage === lang.id ? 'bg-amber-100/60 font-bold text-amber-900' : 'text-stone-700'
                    }`}
                  >
                    <span className="flex items-center gap-2">
                      {currentLanguage === lang.id ? <Check className="w-4 h-4 text-amber-600" /> : <span className="w-4" />}
                      {lang.name}
                    </span>
                    <span className="text-xs text-amber-800 font-bold">{lang.nativeName}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Points & streak */}
          <div className="flex items-center gap-1.5 sm:gap-2 h-9 bg-white border border-amber-200 px-2.5 sm:px-3 rounded-full shadow-sm">
            <div className="flex items-center gap-1 text-amber-800 font-extrabold text-xs sm:text-sm" title="Learning Points">
              <Star className="w-4 h-4 text-amber-500 fill-amber-400" />
              <span>{user?.points || 0}</span>
            </div>
            <div className="w-px h-3.5 bg-amber-200 hidden min-[420px]:block" />
            <div className="items-center gap-1 text-orange-600 font-extrabold text-xs sm:text-sm hidden min-[420px]:flex" title="Active Streak">
              <Flame className="w-4 h-4 text-orange-500 fill-orange-400" />
              <span>{user?.streak || 1}d</span>
            </div>
          </div>

          {/* Profile */}
          <Link
            to="/profile"
            className="flex items-center justify-center w-9 h-9 rounded-full bg-gradient-to-br from-amber-100 to-orange-100 border border-amber-300 hover:from-amber-200 hover:to-orange-200 active:scale-95 text-amber-900 transition-all shadow-sm"
            title="Profile & Passport"
            aria-label="Profile"
          >
            <User className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </header>
  );
};
