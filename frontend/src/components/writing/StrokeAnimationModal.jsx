import React, { useState, useEffect } from 'react';
import { X, Play, RotateCcw, Sparkles } from 'lucide-react';

export const StrokeAnimationModal = ({ targetItem, onClose }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);

  const strokes = targetItem?.strokes || (targetItem?.svg_guide ? [targetItem.svg_guide] : []);
  const totalSteps = strokes.length;

  useEffect(() => {
    let timer;
    if (isPlaying && totalSteps > 0) {
      timer = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= totalSteps - 1) {
            setIsPlaying(false);
            return totalSteps - 1;
          }
          return prev + 1;
        });
      }, 1200);
    }
    return () => clearInterval(timer);
  }, [isPlaying, totalSteps]);

  const handleReplay = () => {
    setCurrentStep(0);
    setIsPlaying(true);
  };

  return (
    <div className="fixed inset-0 z-50 bg-stone-900/60 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200">
      <div className="bg-white border-4 border-amber-300 rounded-3xl p-6 sm:p-8 w-full max-w-md shadow-2xl relative">
        {/* Close Button */}
        <button
          type="button"
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full bg-stone-100 hover:bg-stone-200 text-stone-600 transition-all"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="text-center mb-6">
          <span className="text-xs font-black text-amber-700 uppercase tracking-wider block mb-1">
            ✍️ Step-by-Step Formation
          </span>
          <h2 className="text-2xl font-black text-amber-950">
            Show Me How: '{targetItem?.char}'
          </h2>
          <p className="text-xs font-semibold text-stone-600 mt-1">
            Follow the animated stroke paths to form '{targetItem?.char}' perfectly!
          </p>
        </div>

        {/* Animation Display Stage */}
        <div className="relative w-full aspect-square max-w-[260px] mx-auto bg-amber-50/60 border-2 border-dashed border-amber-300 rounded-3xl p-4 flex items-center justify-center shadow-inner">
          <svg viewBox="0 0 100 100" className="w-full h-full">
            {/* Background Faint Full Guide */}
            {targetItem?.svg_guide && (
              <path
                d={targetItem.svg_guide}
                className="fill-none stroke-amber-200 stroke-[6] stroke-linecap-round stroke-linejoin-round"
              />
            )}

            {/* Completed Strokes up to currentStep */}
            {strokes.slice(0, currentStep + 1).map((pathD, idx) => (
              <path
                key={idx}
                d={pathD}
                className={`fill-none stroke-[7] stroke-linecap-round stroke-linejoin-round transition-all duration-500 ${
                  idx === currentStep ? 'stroke-amber-600 animate-pulse' : 'stroke-amber-950'
                }`}
              />
            ))}
          </svg>

          <div className="absolute bottom-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-amber-200 border border-amber-400 rounded-full text-[11px] font-black text-amber-950 shadow-sm">
            Step {currentStep + 1} of {totalSteps || 1}
          </div>
        </div>

        {/* Control Buttons */}
        <div className="mt-6 flex items-center justify-center gap-3">
          <button
            type="button"
            onClick={handleReplay}
            className="btn-secondary py-2.5 px-4 text-xs font-extrabold"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Replay Animation</span>
          </button>

          {!isPlaying && (
            <button
              type="button"
              onClick={() => setIsPlaying(true)}
              className="btn-primary py-2.5 px-4 text-xs font-extrabold"
            >
              <Play className="w-4 h-4" />
              <span>Play</span>
            </button>
          )}

          <button
            type="button"
            onClick={onClose}
            className="py-2.5 px-5 rounded-2xl bg-amber-500 hover:bg-amber-600 text-white font-extrabold text-xs shadow-md transition-all"
          >
            <span>I'm Ready to Write! ✏️</span>
          </button>
        </div>
      </div>
    </div>
  );
};
