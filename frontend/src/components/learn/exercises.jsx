import React, { useCallback, useRef } from 'react';
import { Volume2, VolumeX } from 'lucide-react';
import { languageToTts } from './audio';

/**
 * Exercise renderers for the Ammachi lesson player.
 * Each receives: { exercise, answer, setAnswer, disabled, revealed, language }
 * and renders the body (~not~ the feedback banner or progress header).
 */

// ---------- Native audio (TTS via backend, speechSynthesis fallback in caller) ----------
const playWithFallback = async (text, language) => {
  if (!text) return;
  try {
    const audio = new Audio(languageToTts(text, language));
    audio.playbackRate = 0.9;
    await audio.play();
  } catch (e) {
    try {
      const u = new SpeechSynthesisUtterance(text);
      u.rate = 0.85;
      window.speechSynthesis.speak(u);
    } catch (e2) {
      console.warn('TTS unavailable:', e2);
    }
  }
};

export const SpeakerButton = ({ text, language, small = false, onPlayed }) => (
  <button
    onClick={async () => {
      await playWithFallback(text, language);
      if (onPlayed) onPlayed();
    }}
    className={`flex items-center justify-center rounded-2xl bg-sky-500 hover:bg-sky-600 text-white border-b-4 border-sky-700 active:border-b-0 active:translate-y-1 transition-all ${
      small ? 'w-10 h-10' : 'w-16 h-16'
    }`}
    aria-label="Play native audio"
  >
    <Volume2 className={small ? 'w-5 h-5' : 'w-8 h-8'} />
  </button>
);

// ---------- Multiple choice ----------
export const MultipleChoice = ({ exercise, answer, setAnswer, disabled, language }) => (
  <div>
    {exercise.native_text && (
      <div className="flex items-center gap-4 mb-7">
        <SpeakerButton text={exercise.native_text} language={language} />
        <span className="font-tamil text-3xl sm:text-4xl font-bold text-stone-800">{exercise.native_text}</span>
        {exercise.transliteration && (
          <span className="text-stone-500 text-sm font-semibold">({exercise.transliteration})</span>
        )}
      </div>
    )}
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {(exercise.options || []).map((opt, idx) => (
        <button
          key={idx}
          disabled={disabled}
          onClick={() => setAnswer(idx)}
          className={`text-left font-bold text-lg rounded-2xl px-5 py-4 border-2 border-b-4 transition-all active:border-b-2 active:translate-y-0.5 ${
            answer === idx
              ? 'bg-sky-100 border-sky-400 text-sky-900'
              : 'bg-white border-stone-200 text-stone-700 hover:bg-stone-50'
          }`}
        >
          <span className="mr-2 text-stone-400 font-black">{idx + 1}.</span>
          {opt}
        </button>
      ))}
    </div>
  </div>
);

// ---------- Translate (word bank) ----------
export const TranslateWordBank = ({ exercise, answer, setAnswer, disabled, language }) => {
  const selected = answer || [];
  const bank = exercise.bank || [];
  const toggle = (word) => {
    if (disabled) return;
    if (selected.includes(word)) setAnswer(selected.filter((w) => w !== word));
    else setAnswer([...selected, word]);
  };
  return (
    <div>
      <div className="flex items-center gap-4 mb-6">
        <SpeakerButton text={(exercise.native_text || '').split(' (')[0]} language={language} />
        <span className="font-tamil text-3xl font-bold text-stone-800">{exercise.native_text}</span>
      </div>

      {/* Answer area */}
      <div className="min-h-[74px] rounded-2xl border-2 border-dashed border-stone-300 p-2 mb-5">
        <div className="flex flex-wrap gap-2">
          {selected.map((w, i) => (
            <button
              key={`${w}-${i}`}
              disabled={disabled}
              onClick={() => toggle(w)}
              className="bg-sky-100 border-2 border-sky-300 border-b-4 text-sky-900 font-bold px-4 py-2 rounded-xl active:border-b-2"
            >
              {w}
            </button>
          ))}
        </div>
      </div>

      {/* Word bank */}
      <div className="flex flex-wrap gap-2">
        {bank.map((w, i) => (
          <button
            key={`${w}-${i}`}
            disabled={disabled || selected.includes(w)}
            onClick={() => toggle(w)}
            className="bg-white border-2 border-stone-200 border-b-4 text-stone-700 font-bold px-4 py-2 rounded-xl hover:bg-stone-50 disabled:opacity-30"
          >
            {w}
          </button>
        ))}
      </div>
    </div>
  );
};

// ---------- Listen ----------
export const ListenExercise = ({ exercise, answer, setAnswer, disabled, language }) => (
  <div>
    <div className="flex flex-col items-center gap-4 mb-7">
      <SpeakerButton
        text={exercise.native_text}
        language={language}
      />
      {exercise.transliteration && (
        <span className="text-sm font-semibold text-stone-500">Hint: it starts with “{exercise.transliteration.slice(0, 4)}…”</span>
      )}
    </div>
    <div className="grid grid-cols-1 gap-3">
      {(exercise.options || []).map((opt, idx) => (
        <button
          key={idx}
          disabled={disabled}
          onClick={() => setAnswer(idx)}
          className={`text-left font-bold text-lg rounded-2xl px-5 py-4 border-2 border-b-4 transition-all ${
            answer === idx ? 'bg-sky-100 border-sky-400 text-sky-900' : 'bg-white border-stone-200 text-stone-700'
          }`}
        >
          {opt}
        </button>
      ))}
    </div>
  </div>
);

// ---------- Match pairs ----------
export const MatchPairs = ({ exercise, answer, setAnswer, disabled, onMistake }) => {
  // local state: selection & matched set live here; final answer = mistakes count <= MAX (send mapping) else null
  const [pending, setPending] = React.useState(null);           // selected native word
  const [matched, setMatched] = React.useState([]);             // english strings matched
  const [wrongFlash, setWrongFlash] = React.useState(null);
  const [mistakes, setMistakes] = React.useState(0);

  const pairs = exercise.pairs || [];
  const tiles = React.useMemo(() => {
    const arr = [
      ...pairs.map((p) => ({ id: `n-${p.native}`, kind: 'native', label: p.native, translit: p.translit, pair: p })),
      ...pairs.map((p) => ({ id: `e-${p.english}`, kind: 'english', label: p.english, translit: null, pair: p })),
    ];
    // deterministic shuffle
    for (let i = arr.length - 1; i > 0; i--) {
      const j = (i * 7 + 3) % (i + 1);
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }, [exercise.id]);

  const finishIfDone = (matchedList, mErrors) => {
    if (matchedList.length === pairs.length) {
      setAnswer(mErrors > 3 ? null : Object.fromEntries(pairs.map((p) => [p.native, p.english])));
    }
  };

  const tapTile = (tile) => {
    if (disabled || matched.includes(tile.pair.english)) return;
    if (tile.kind === 'native') {
      setPending(pending === tile.id ? null : tile.id);
      return;
    }
    // english tile
    if (!pending) return;
    const nativeTile = tiles.find((t) => t.id === pending);
    if (nativeTile.pair.native === tile.pair.native) {
      const next = [...matched, tile.pair.english];
      setMatched(next);
      setPending(null);
      finishIfDone(next, mistakes);
    } else {
      setPending(null);
      const m = mistakes + 1;
      setMistakes(m);
      setWrongFlash(tile.id);
      if (onMistake) onMistake();
      setTimeout(() => setWrongFlash(null), 500);
      finishIfDone(matched, m);
    }
  };

  return (
    <div className="grid grid-cols-2 gap-3 max-w-md mx-auto">
      {tiles.map((tile) => {
        const isMatched = tile.kind === 'english' && matched.includes(tile.pair.english);
        const isNativeMatched = tile.kind === 'native' && matched.includes(tile.pair.english);
        const gone = isMatched || isNativeMatched ? 'opacity-0 pointer-events-none scale-90' : '';
        const sel = tile.id === pending ? 'ring-4 ring-sky-400 bg-sky-50 border-sky-400' : '';
        const flash = wrongFlash === tile.id ? 'ring-4 ring-rose-400 bg-rose-50 border-rose-400 shake' : '';
        return (
          <button
            key={tile.id}
            onClick={() => tapTile(tile)}
            className={`rounded-2xl border-2 border-b-4 px-3 py-3.5 font-bold transition-all duration-200 ${
              tile.kind === 'native' ? 'font-tamil text-xl' : 'text-base'
            } bg-white border-stone-200 text-stone-700 hover:bg-stone-50 ${sel} ${flash} ${gone}`}
          >
            {tile.label}
            {tile.translit && <span className="block text-[11px] font-semibold text-stone-400">{tile.translit}</span>}
          </button>
        );
      })}
    </div>
  );
};

// ---------- Speak ----------
export const SpeakExercise = ({ exercise, language, onResult }) => {
  const [recording, setRecording] = React.useState(false);
  const [status, setStatus] = React.useState('idle'); // idle | recording | checking | done | error
  const [feedback, setFeedback] = React.useState('');
  const mediaRef = React.useRef(null);

  const startRecording = async () => {
    try {
      setStatus('recording');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];
      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(chunks, { type: 'audio/webm' });
        setStatus('checking');
        try {
          const { voiceService } = await import('../../services/voiceService');
          const result = await voiceService.analyzeVoice(
            blob,
            exercise.native_text || '',
            exercise.transliteration || '',
            exercise.english || '',
            language,
          );
          const ok = (result?.score ?? result?.accuracy ?? 60) >= 50;
          setFeedback(ok ? (result?.feedback || 'Amma is proud! 🌟') : (result?.feedback || 'Kolla! Try again 🌱'));
          setStatus('done');
          onResult(ok, true);
        } catch (err) {
          setStatus('error');
          setFeedback('Mic unavailable. You can skip speaking.');
        }
      };
      mediaRef.current = recorder;
      recorder.start();
      // auto-stop after 4.5s like a kid-friendly push-to-talk
      setTimeout(() => recorder.state !== 'inactive' && recorder.stop(), 4000);
    } catch (err) {
      setStatus('error');
      setFeedback('Microphone not available. You can skip speaking, kanna.');
    }
  };

  return (
    <div className="flex flex-col items-center gap-5">
      <div className="flex items-center gap-4">
        <SpeakerButton text={exercise.native_text} language={language} />
        <span className="font-tamil text-3xl font-bold text-stone-800">{exercise.native_text}</span>
      </div>
      <span className="text-stone-500 text-sm font-semibold">{exercise.transliteration} — “{exercise.english}”</span>

      {status !== 'done' && status !== 'error' && (
        <button
          onClick={recording ? undefined : startRecording}
          disabled={status === 'checking'}
          className={`flex flex-col items-center gap-2 w-44 h-44 rounded-full border-4 transition-all ${
            status === 'recording'
              ? 'bg-rose-100 border-rose-400 animate-pulse'
              : 'bg-sky-50 border-sky-400 hover:bg-sky-100 active:scale-95'
          }`}
        >
          {status === 'recording' && <VolumeX className="w-10 h-10 text-rose-500" />}
          <span className="mt-4 font-black text-sky-700 uppercase tracking-wider text-sm">
            {status === 'recording' ? 'Listening…' : status === 'checking' ? 'Checking…' : 'Tap to speak 🎤'}
          </span>
        </button>
      )}

      {(status === 'done' || status === 'error') && (
        <div className="text-center">
          <p className="font-bold text-lg text-stone-700">{feedback}</p>
          {status === 'error' && (
            <button
              onClick={startRecording}
              className="mt-3 btn-primary text-sm"
            >
              Try again
            </button>
          )}
        </div>
      )}
    </div>
  );
};
