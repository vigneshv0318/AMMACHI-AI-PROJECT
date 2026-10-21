import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { X, Heart, Flower2, Gem, Check, Zap } from 'lucide-react';
import { learnService } from '../services/learnService';
import { useLanguage } from '../context/LanguageContext';
import { AmmachiMascot } from '../components/common/AmmachiMascot';
import { triggerCelebration } from '../components/common/Confetti';
import { MultipleChoice, TranslateWordBank, ListenExercise, MatchPairs, SpeakExercise } from '../components/learn/exercises';

/**
 * Full-screen Duolingo-style lesson player.
 * Receives attempt state via react-router location.state (from LearnPathPage intro modal).
 */
export const LessonPlayerPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { currentLanguage } = useLanguage();
  const state = location.state || {};

  const [exercises, setExercises] = useState(state.exercises || []);
  const attemptIdRef = useRef(state.attemptId || null);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState(null);
  const [matching, setMatching] = useState(false);        // true while exercise type = match (answer computed locally)
  const [feedback, setFeedback] = useState(null);        // {correct, explanation, correctAnswer}
  const [hearts, setHearts] = useState(state.hearts ?? 5);
  const [outOfHearts, setOutOfHearts] = useState(false);
  const [combo, setCombo] = useState(0);
  const [comboFlash, setComboFlash] = useState(0);
  const [checking, setChecking] = useState(false);
  const [result, setResult] = useState(null);            // celebration screen data
  const [quitConfirm, setQuitConfirm] = useState(false);

  const exercise = exercises[index];
  const total = exercises.length;

  useEffect(() => {
    if (!attemptIdRef.current || !exercises.length) {
      navigate('/learn', { replace: true });
    }
  }, []);

  // Scroll to top on exercise change
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [index]);

  const canCheck = useMemo(() => {
    if (!exercise) return false;
    if (exercise.type === 'match') return answer !== null && answer !== undefined;
    if (exercise.type === 'speak') return false; // answered via mic flow
    return answer !== null && answer !== undefined
      && (Array.isArray(answer) ? answer.length > 0 : true);
  }, [exercise, answer]);

  const progressPct = Math.round((index / Math.max(1, total)) * 100);

  const handleCheck = async () => {
    if (!exercise || checking) return;
    setChecking(true);
    try {
      const resp = await learnService.checkAnswer(attemptIdRef.current, exercise.id, answer);
      setFeedback(resp);
      setHearts(resp.hearts);
      if (resp.combo_current >= 0 && resp.xp_gained > 0) {
        setComboFlash(resp.xp_gained);
        setTimeout(() => setComboFlash(0), 1800);
      }
      if (resp.out_of_hearts) {
        setOutOfHearts(true);
      }
    } catch (err) {
      console.warn('Answer check failed:', err);
      setFeedback({ correct: false, explanation: 'Network hiccup — try again, kanna.' });
    } finally {
      setChecking(false);
    }
  };

  const nextAction = () => {
    setFeedback(null);
    setAnswer(null);
    if (!outOfHearts && index + 1 < total) {
      setIndex((i) => i + 1);
    } else if (outOfHearts) {
      handleQuit(true); // hearts exhausted — leave lesson
    } else {
      finish();
    }
  };

  const finish = async () => {
    try {
      const summary = await learnService.completeAttempt(attemptIdRef.current);
      setResult(summary);
      triggerCelebration();
      window.dispatchEvent(new Event('ammachi-hud-refresh'));
    } catch (err) {
      console.warn('Complete failed:', err);
      navigate('/learn');
    }
  };

  const handleQuit = async (skipConfirm = false) => {
    if (!skipConfirm && !quitConfirm) {
      setQuitConfirm(true);
      return;
    }
    setQuitConfirm(false);
    try {
      if (attemptIdRef.current) await learnService.quitAttempt(attemptIdRef.current);
    } catch { /* best-effort */ }
    navigate('/learn');
  };

  const skipSpeak = () => {
    // Duolingo behavior: speaking exercise can be skipped without heart loss
    handleSpeakResult(true, false, true);
  };

  const handleSpeakResult = async (spokenOk, _analyzed = false, isSkip = false) => {
    // For skipped speech, tell the server it was fine (like "can't speak now")
    const serverAns = isSkip ? true : spokenOk;
    try {
      const resp = await learnService.checkAnswer(attemptIdRef.current, exercise.id, serverAns);
      setFeedback({ ...resp, explanation: isSkip ? 'Speaking skipped — no worries!' : resp.explanation });
      setHearts(resp.hearts);
      if (resp.out_of_hearts) setOutOfHearts(true);
    } catch {
      setFeedback({ correct: true, explanation: '' });
    }
  };

  // ================= Celebration screen =================
  if (result) {
    return (
      <div className="fixed inset-0 z-50 bg-gradient-to-b from-amber-50 to-orange-50 flex flex-col items-center justify-center p-6 overflow-auto">
        <AmmachiMascot size="xl" speaking />
        <h1 className="mt-5 text-3xl font-black text-amber-900 text-center">
          {result.perfect_bonus > 0 ? 'Perfect lesson! 🌟' : 'Lesson complete! 🎉'}
        </h1>
        <p className="font-bold text-amber-700 mt-1">
          {result.correct}/{result.total} correct · {result.combo_max >= 5 ? `Best combo ×${result.combo_max}! ` : ''}Ammachi is proud!
        </p>

        {/* XP break-down */}
        <div className="mt-6 w-full max-w-sm bg-white rounded-3xl border-2 border-amber-200 shadow-md p-5 divide-y divide-amber-100">
          <RewardRow icon={<Zap className="w-5 h-5 text-amber-500" />} label="Base XP" value={result.base_xp} />
          {result.perfect_bonus > 0 && (
            <RewardRow icon={<Flower2 className="w-5 h-5 text-emerald-500" />} label="Perfect bonus" value={result.perfect_bonus} />
          )}
          {result.combo_bonus > 0 && (
            <RewardRow icon={<FlameIcon />} label={`Combo bonus (×${result.combo_max})`} value={result.combo_bonus} />
          )}
          <RewardRow icon={<Zap className="w-5 h-5 text-blue-500" />} label="Total XP" value={result.xp_total} highlight />
          <RewardRow icon={<Gem className="w-5 h-5 text-cyan-500" />} label="Gems" value={result.gems} />
          <RewardRow
            icon={<FlameIcon />}
            label={result.streak_state === 'extended' ? `Streak extended → ${result.streak}!` : `${result.streak} day streak`}
            value={result.streak}
          />
        </div>

        {/* Stars */}
        <div className="mt-5 flex gap-1">
          {[...Array(3)].map((_, i) => (
            <span key={i} className={`text-4xl ${i < result.stars ? '' : 'grayscale opacity-25'}`}>⭐</span>
          ))}
        </div>

        <button onClick={() => navigate('/learn')} className="mt-8 w-full max-w-xs btn-primary text-lg">
          Continue
        </button>
      </div>
    );
  }

  // ================= Out of hearts modal =================
  if (outOfHearts) {
    return (
      <div className="fixed inset-0 z-50 bg-stone-900/60 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl p-7 max-w-sm w-full text-center border-2 border-rose-200 shadow-2xl">
          <div className="text-6xl mb-3">💔</div>
          <h2 className="text-2xl font-black text-stone-800">Out of hearts!</h2>
          <p className="text-stone-600 font-semibold mt-2">
            You ran out of hearts. Refill them in the shop or wait ~30 min for a free heart, kanna.
          </p>
          <div className="flex gap-2 mt-6">
            <button
              onClick={async () => { try { await learnService.quitAttempt(attemptIdRef.current); } catch {} navigate('/shop'); }}
              className="flex-1 btn-primary"
            >
              Go to shop
            </button>
            <button onClick={() => navigate('/learn')} className="flex-1 bg-stone-100 hover:bg-stone-200 text-stone-700 font-black rounded-2xl py-3">
              Back home
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!exercise) return null;

  const progress = Math.round((((feedback && !feedback.correct) ? index + 1 : index) / total) * 100);

  return (
    <div className="fixed inset-0 z-50 bg-warmbg flex flex-col">
      {/* Header: progress + hearts */}
      <header className="pt-safe shrink-0">
        <div className="max-w-2xl mx-auto w-full relative flex items-center gap-3 px-4 pt-3 pb-2">
          <button
            onClick={() => handleQuit()}
            className="p-2 rounded-full hover:bg-stone-200/70 text-stone-500"
            aria-label="Exit lesson"
          >
            <X className="w-6 h-6" />
          </button>

          <div className="flex-1 h-4 bg-stone-300/60 rounded-full overflow-hidden relative">
            <div
              className="h-full bg-gradient-to-r from-green-400 to-emerald-500 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>

          <div className="flex items-center gap-1 font-black text-rose-600" title={`${hearts} hearts left`}>
            <Heart className={`w-5 h-5 ${hearts > 0 ? 'fill-rose-500 text-rose-500' : 'text-stone-300'}`} />
            <span>{hearts}</span>
          </div>

          {comboFlash > 0 && (
            <span className="absolute right-24 top-14 bg-amber-400 text-amber-950 font-black text-xs px-2 py-1 rounded-full shadow animate-bounce">
              +{comboFlash} combo XP!
            </span>
          )}
        </div>
      </header>

      {/* Exercise body */}
      <main className="flex-1 overflow-y-auto no-scrollbar">
        <div className="max-w-2xl mx-auto w-full px-4 pt-4 pb-40">
          <h2 className="text-lg sm:text-2xl font-black text-amber-900 mb-5">{exercise.prompt}</h2>

          {exercise.type === 'multiple_choice' && (
            <MultipleChoice exercise={exercise} answer={answer} setAnswer={setAnswer} disabled={!!feedback} language={currentLanguage} />
          )}
          {exercise.type === 'translate' && (
            <TranslateWordBank exercise={exercise} answer={answer} setAnswer={setAnswer} disabled={!!feedback} language={currentLanguage} />
          )}
          {exercise.type === 'listen' && (
            <ListenExercise exercise={exercise} answer={answer} setAnswer={setAnswer} disabled={!!feedback} language={currentLanguage} />
          )}
          {exercise.type === 'match' && (
            <MatchPairs
              exercise={exercise}
              answer={answer}
              setAnswer={setAnswer}
              disabled={!!feedback}
              language={currentLanguage}
            />
          )}
          {exercise.type === 'speak' && (
            <SpeakExercise exercise={exercise} language={currentLanguage} onResult={(ok) => handleSpeakResult(ok)} />
          )}
        </div>
      </main>

      {/* Footer: check / feedback */}
      <footer className="shrink-0 border-t-2 border-stone-200 bg-white">
        {feedback ? (
          <div className={`max-w-2xl mx-auto w-full p-4 ${feedback.correct ? 'bg-emerald-50' : 'bg-rose-50'}`}>
            <div className="flex items-start gap-3">
              <span className={`flex items-center justify-center w-10 h-10 rounded-full shrink-0 ${feedback.correct ? 'bg-emerald-500' : 'bg-rose-500'} text-white`}>
                {feedback.correct ? <Check className="w-6 h-6" strokeWidth={3} /> : <X className="w-6 h-6" strokeWidth={3} />}
              </span>
              <div className="flex-1 min-w-0">
                <p className={`font-black text-lg ${feedback.correct ? 'text-emerald-700' : 'text-rose-700'}`}>
                  {feedback.correct ? 'Correct! Sari!' : 'Oops — not quite'}
                </p>
                <p className="text-sm font-semibold text-stone-600">
                  {feedback.explanation || ''}
                  {!feedback.correct && feedback.correct_answer != null && (
                    <span className="block mt-0.5">
                      Correct answer:{' '}
                      <b>
                        {Array.isArray(feedback.correct_answer)
                          ? feedback.correct_answer.join(' ')
                          : typeof feedback.correct_answer === 'string'
                            ? feedback.correct_answer
                            : ''}
                      </b>
                    </span>
                  )}
                </p>
              </div>
              <button
                onClick={nextAction}
                className="shrink-0 px-6 py-3 rounded-2xl font-black text-white bg-emerald-500 border-b-4 border-emerald-700 active:border-b-0 active:translate-y-1 hover:brightness-105"
              >
                {outOfHearts ? 'Finish' : index + 1 < total ? 'Continue' : 'Finish'}
              </button>
            </div>
          </div>
        ) : (
          <div className="max-w-2xl mx-auto w-full p-4 flex items-center gap-3">
            <button
              onClick={() => handleQuit()}
              className="text-stone-500 font-black px-4 py-3 rounded-2xl hover:bg-stone-100"
            >
              Quit
            </button>
            <div className="flex-1" />
            {exercise.type === 'speak' ? (
              <button
                onClick={skipSpeak}
                className="px-5 py-3 font-black text-stone-500 underline underline-offset-2"
              >
                Can't speak now
              </button>
            ) : null}
            <button
              onClick={handleCheck}
              disabled={!canCheck || checking}
              className="px-7 py-3 rounded-2xl font-black text-white uppercase tracking-wide bg-sky-500 border-b-4 border-sky-700 active:border-b-0 active:translate-y-1 hover:brightness-105 disabled:opacity-40 disabled:active:border-b-4 disabled:active:translate-y-0"
            >
              Check
            </button>
          </div>
        )}
      </footer>

      {/* Quit confirm */}
      {quitConfirm && (
        <div className="fixed inset-0 z-[60] bg-stone-900/50 flex items-center justify-center p-4" onClick={() => setQuitConfirm(false)}>
          <div className="bg-white rounded-3xl p-6 max-w-sm w-full text-center border-2 border-amber-200" onClick={(e) => e.stopPropagation()}>
            <AmmachiMascot size="md" speaking />
            <h3 className="mt-3 text-xl font-black text-stone-800">Leave the lesson?</h3>
            <p className="text-sm font-semibold text-stone-600 mt-1">Your progress in this lesson will be lost, kanna.</p>
            <div className="flex gap-2 mt-5">
              <button onClick={() => setQuitConfirm(false)} className="flex-1 bg-stone-100 hover:bg-stone-200 font-black rounded-2xl py-3">
                Keep learning
              </button>
              <button onClick={handleQuit} className="flex-1 bg-rose-500 hover:bg-rose-600 text-white font-black rounded-2xl py-3">
                Quit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const FlameIcon = () => <span className="font-black text-orange-500 text-lg leading-none">🔥</span>;

const RewardRow = ({ icon, label, value, highlight = false }) => (
  <div className={`flex items-center gap-3 py-2.5 ${highlight ? 'font-black text-amber-900' : 'font-bold text-stone-700'}`}>
    <span className="shrink-0">{icon}</span>
    <span className="flex-1">{label}</span>
    <span className="tabular-nums">+{value}</span>
  </div>
);
