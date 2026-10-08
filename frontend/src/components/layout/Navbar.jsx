import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Flame, Star, Globe, User, LogOut, ChevronDown, Award } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { AmmachiMascot } from '../common/AmmachiMascot';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const { currentLanguage, setLanguage, languages, activeLangMeta } = useLanguage();
  const [langMenuOpen, setLangMenuOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-40 bg-warmbg/95 backdrop-blur border-b border-amber-200/70 px-4 sm:px-6 py-3 transition-all">
      <div className="max-w-6xl mx-auto flex items-center justify-between gap-4">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-3 group">
          <AmmachiMascot size="sm" />
          <div className="flex flex-col">
            <span className="text-xl sm:text-2xl font-black text-amber-900 tracking-tight group-hover:text-amber-600 transition-colors">
              Ammachi's Class
            </span>
            <span className="text-xs font-semibold text-amber-700/80 -mt-1 hidden sm:block">
              {activeLangMeta.greeting}
            </span>
          </div>
        </Link>

        {/* Center/Right Items */}
        <div className="flex items-center gap-2 sm:gap-4">
          {/* Language Selector Dropdown */}
          <div className="relative">
            <button
              onClick={() => setLangMenuOpen(!langMenuOpen)}
              type="button"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-100/80 hover:bg-amber-200 text-amber-900 font-bold text-xs sm:text-sm border border-amber-300 shadow-sm transition-all"
            >
              <Globe className="w-3.5 h-3.5 text-amber-700" />
              <span>{activeLangMeta.nativeName}</span>
              <ChevronDown className="w-3 h-3 text-amber-700" />
            </button>

            {langMenuOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white border-2 border-amber-200 rounded-2xl shadow-xl py-2 z-50 animate-in fade-in zoom-in-95 duration-150">
                <div className="px-3 py-1 text-xs font-bold text-stone-500 uppercase tracking-wider">
                  Select Language
                </div>
                {languages.map((lang) => (
                  <button
                    key={lang.id}
                    onClick={() => {
                      setLanguage(lang.id);
                      setLangMenuOpen(false);
                    }}
                    className={`w-full text-left px-4 py-2 text-sm flex items-center justify-between hover:bg-amber-50 transition-colors ${
                      currentLanguage === lang.id ? 'bg-amber-100/60 font-bold text-amber-900' : 'text-stone-700'
                    }`}
                  >
                    <span>{lang.name}</span>
                    <span className="text-xs text-amber-800 font-bold">{lang.nativeName}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Gamification Stats Pill */}
          <div className="flex items-center gap-2 bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-full shadow-inner">
            {/* Points */}
            <div className="flex items-center gap-1 text-amber-800 font-extrabold text-xs sm:text-sm" title="Learning Points">
              <Star className="w-4 h-4 text-amber-500 fill-amber-400" />
              <span>{user?.points || 0}</span>
            </div>

            <div className="w-px h-3.5 bg-amber-200" />

            {/* Streak */}
            <div className="flex items-center gap-1 text-orange-600 font-extrabold text-xs sm:text-sm" title="Active Streak">
              <Flame className="w-4 h-4 text-orange-500 fill-orange-400 animate-pulse" />
              <span>{user?.streak || 1}d</span>
            </div>
          </div>

          {/* Profile / Logout */}
          <Link
            to="/profile"
            className="flex items-center justify-center w-9 h-9 rounded-full bg-amber-100 border border-amber-300 hover:bg-amber-200 text-amber-900 transition-all shadow-sm"
            title="Profile & Passport"
          >
            <User className="w-4 h-4 text-amber-900" />
          </Link>
        </div>
      </div>
    </header>
  );
};
