import React from 'react';
import { ChevronLeft, ChevronRight, BookOpen, Layers, Sparkles } from 'lucide-react';

export const CurriculumBrowser = ({
  language = 'Tamil',
  curriculum = [],
  selectedItem,
  onSelectItem,
  activeLevel = 1,
  onSelectLevel
}) => {
  const levels = [
    { level: 1, label: 'L1: Vowels', desc: 'Basic Sound Foundations' },
    { level: 2, label: 'L2: Consonants', desc: 'Primary Alphabet' },
    { level: 3, label: 'L3: Uyirmei', desc: 'Combinations & Diacritics' },
    { level: 4, label: 'L4: Words', desc: 'Vocabulary Practice' },
    { level: 5, label: 'L5: Sentences', desc: 'Fluency Practice' }
  ];

  const currentLevelItems = curriculum.filter(item => (item.level || 1) === activeLevel);
  const selectedIndex = currentLevelItems.findIndex(item => item.char === selectedItem?.char);

  const handlePrev = () => {
    if (selectedIndex > 0) {
      onSelectItem(currentLevelItems[selectedIndex - 1]);
    }
  };

  const handleNext = () => {
    if (selectedIndex < currentLevelItems.length - 1) {
      onSelectItem(currentLevelItems[selectedIndex + 1]);
    }
  };

  return (
    <div className="bg-white border-2 border-amber-200 rounded-3xl p-4 sm:p-5 shadow-sm space-y-4">
      {/* Level Selection Tabs */}
      <div className="flex items-center justify-between gap-2 overflow-x-auto pb-1 scrollbar-none">
        {levels.map((lvl) => (
          <button
            key={lvl.level}
            type="button"
            onClick={() => onSelectLevel(lvl.level)}
            className={`flex flex-col items-center py-2 px-3 rounded-2xl border-2 transition-all whitespace-nowrap select-none ${
              activeLevel === lvl.level
                ? 'bg-amber-400 border-amber-600 text-amber-950 font-black shadow-sm scale-102'
                : 'bg-amber-50/60 border-amber-200 text-stone-600 hover:border-amber-300 font-bold'
            }`}
          >
            <span className="text-xs font-black">{lvl.label}</span>
            <span className="text-[10px] opacity-80 mt-0.5 font-medium">{lvl.desc}</span>
          </button>
        ))}
      </div>

      {/* Level Items Grid & Step Navigator */}
      <div className="flex items-center justify-between gap-3 bg-amber-50/70 p-3 rounded-2xl border border-amber-200">
        <button
          type="button"
          onClick={handlePrev}
          disabled={selectedIndex <= 0}
          className="p-2 rounded-xl bg-white border border-amber-300 text-amber-900 disabled:opacity-30 hover:bg-amber-100 transition-all shadow-xs"
          title="Previous Character"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>

        {/* Horizontal Character / Word Pills */}
        <div className="flex items-center gap-2 overflow-x-auto py-1 scrollbar-none max-w-full">
          {currentLevelItems.map((item) => (
            <button
              key={item.char}
              type="button"
              onClick={() => onSelectItem(item)}
              className={`py-1.5 px-3 rounded-xl border font-black text-sm transition-all whitespace-nowrap ${
                selectedItem?.char === item.char
                  ? 'bg-amber-500 text-white border-amber-600 shadow-sm scale-105'
                  : 'bg-white text-stone-800 border-amber-200 hover:border-amber-400'
              }`}
            >
              {item.char}
            </button>
          ))}
        </div>

        <button
          type="button"
          onClick={handleNext}
          disabled={selectedIndex < 0 || selectedIndex >= currentLevelItems.length - 1}
          className="p-2 rounded-xl bg-white border border-amber-300 text-amber-900 disabled:opacity-30 hover:bg-amber-100 transition-all shadow-xs"
          title="Next Character"
        >
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>

      {/* Step Counter Indicator */}
      <div className="flex items-center justify-between text-xs font-bold text-stone-500 px-1">
        <span>Language: <strong className="text-amber-900">{language}</strong></span>
        <span>
          Lesson {selectedIndex >= 0 ? selectedIndex + 1 : 1} of {currentLevelItems.length || 1}
        </span>
      </div>
    </div>
  );
};
