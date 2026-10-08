import React, { useEffect, useState } from 'react';
import { Download, X, Share, SquarePlus, MoreVertical, Smartphone, CheckCircle2 } from 'lucide-react';
import { canPromptInstall, getPlatform, isStandalone, promptInstall, subscribeInstall } from '../../utils/pwaInstall';

const DISMISS_KEY = 'ammachi_install_dismissed_at';
const DISMISS_DAYS = 3;

const readDismissed = () => {
  try {
    const at = Number(localStorage.getItem(DISMISS_KEY) || 0);
    return at && Date.now() - at < DISMISS_DAYS * 24 * 60 * 60 * 1000;
  } catch {
    return false;
  }
};

export const useInstallState = () => {
  const [canPrompt, setCanPrompt] = useState(canPromptInstall());
  const [installed, setInstalled] = useState(isStandalone());

  useEffect(() => {
    const unsubscribe = subscribeInstall(() => setCanPrompt(canPromptInstall()));
    const mq = window.matchMedia?.('(display-mode: standalone)');
    const onChange = () => setInstalled(isStandalone());
    mq?.addEventListener?.('change', onChange);
    window.addEventListener('appinstalled', onChange);
    return () => {
      unsubscribe();
      mq?.removeEventListener?.('change', onChange);
      window.removeEventListener('appinstalled', onChange);
    };
  }, []);

  return { canPrompt, installed, platform: getPlatform() };
};

const Steps = ({ platform }) => {
  if (platform === 'ios' || platform === 'ios-inapp') {
    return (
      <ol className="space-y-3 text-sm font-semibold text-stone-700">
        {platform === 'ios-inapp' && (
          <li className="rounded-xl bg-amber-50 border border-amber-200 p-3 text-amber-900">
            First open this page in <b>Safari</b> (tap ••• → "Open in Safari").
          </li>
        )}
        <li className="flex items-center gap-3">
          <span className="flex shrink-0 w-8 h-8 items-center justify-center rounded-full bg-blue-100 text-blue-600"><Share className="w-4 h-4" /></span>
          <span>Tap the <b>Share</b> button in Safari's toolbar.</span>
        </li>
        <li className="flex items-center gap-3">
          <span className="flex shrink-0 w-8 h-8 items-center justify-center rounded-full bg-stone-100 text-stone-700"><SquarePlus className="w-4 h-4" /></span>
          <span>Scroll down and tap <b>Add to Home Screen</b>.</span>
        </li>
        <li className="flex items-center gap-3">
          <span className="flex shrink-0 w-8 h-8 items-center justify-center rounded-full bg-emerald-100 text-emerald-700"><CheckCircle2 className="w-4 h-4" /></span>
          <span>Tap <b>Add</b>. Ammachi appears on your home screen!</span>
        </li>
      </ol>
    );
  }
  return (
    <ol className="space-y-3 text-sm font-semibold text-stone-700">
      <li className="flex items-center gap-3">
        <span className="flex shrink-0 w-8 h-8 items-center justify-center rounded-full bg-stone-100 text-stone-700"><MoreVertical className="w-4 h-4" /></span>
        <span>Open your browser menu (<b>⋮</b> at the top right).</span>
      </li>
      <li className="flex items-center gap-3">
        <span className="flex shrink-0 w-8 h-8 items-center justify-center rounded-full bg-amber-100 text-amber-700"><Smartphone className="w-4 h-4" /></span>
        <span>Tap <b>Install app</b> or <b>Add to Home screen</b>.</span>
      </li>
      <li className="flex items-center gap-3">
        <span className="flex shrink-0 w-8 h-8 items-center justify-center rounded-full bg-emerald-100 text-emerald-700"><CheckCircle2 className="w-4 h-4" /></span>
        <span>Confirm with <b>Install</b>.</span>
      </li>
    </ol>
  );
};

const InstructionsSheet = ({ platform, onClose }) => (
  <div className="fixed inset-0 z-[60] flex items-end sm:items-center justify-center bg-black/40 p-0 sm:p-4" onClick={onClose} role="dialog" aria-modal="true" aria-label="How to install">
    <div
      className="w-full sm:max-w-sm bg-white rounded-t-3xl sm:rounded-3xl p-5 pb-[calc(1.25rem+env(safe-area-inset-bottom))] shadow-2xl animate-in slide-in-from-bottom-4"
      onClick={(e) => e.stopPropagation()}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <img src="/pwa-192x192.png" alt="" className="w-11 h-11 rounded-2xl" />
          <div>
            <p className="font-black text-amber-950 leading-tight">Install Ammachi</p>
            <p className="text-xs font-semibold text-stone-500">Learn like a real app, even offline</p>
          </div>
        </div>
        <button onClick={onClose} className="p-2 rounded-full hover:bg-stone-100 text-stone-500" aria-label="Close">
          <X className="w-5 h-5" />
        </button>
      </div>
      <Steps platform={platform} />
      <button onClick={onClose} className="btn-primary w-full mt-5">Got it</button>
    </div>
  </div>
);

/**
 * Install call-to-action.
 * variant="banner": floating card (auto-hides after "Not now" for a few days)
 * variant="card":   always-visible inline card, e.g. on the profile page
 */
export const InstallPrompt = ({ variant = 'banner', aboveBottomNav = false, alwaysShow = false, className = '' }) => {
  const { canPrompt, installed, platform } = useInstallState();
  const [dismissed, setDismissed] = useState(readDismissed());
  const [showSteps, setShowSteps] = useState(false);
  const [justInstalled, setJustInstalled] = useState(false);

  if (installed || justInstalled) {
    return variant === 'card' && alwaysShow ? (
      <div className="flex items-center gap-3 rounded-2xl border-2 border-emerald-200 bg-emerald-50 p-4 text-emerald-900 font-bold text-sm">
        <CheckCircle2 className="w-5 h-5 shrink-0" /> Ammachi is installed on this device.
      </div>
    ) : null;
  }
  if (variant === 'banner' && dismissed) return null;
  // Desktop browsers without an install prompt (Firefox, Safari on Mac) can't install, so don't nag
  if (platform === 'desktop' && !canPrompt && !alwaysShow) return null;

  const handleInstall = async () => {
    if (canPrompt) {
      const outcome = await promptInstall();
      if (outcome === 'accepted') setJustInstalled(true);
      else if (outcome === 'unavailable') setShowSteps(true);
    } else {
      setShowSteps(true);
    }
  };

  const handleDismiss = () => {
    try {
      localStorage.setItem(DISMISS_KEY, String(Date.now()));
    } catch {
      /* storage unavailable: just hide for this session */
    }
    setDismissed(true);
  };

  const body = (
    <div className="flex items-center gap-3">
      <img src="/pwa-192x192.png" alt="" className="w-11 h-11 rounded-2xl shadow-sm shrink-0" />
      <div className="min-w-0 flex-1">
        <p className="font-black text-amber-950 text-sm leading-tight">Install Ammachi app</p>
        <p className="text-xs font-semibold text-stone-600 leading-snug mt-0.5">
          Opens full screen and works offline
        </p>
      </div>
      <button
        onClick={handleInstall}
        className="shrink-0 inline-flex items-center gap-1.5 px-3.5 h-10 rounded-full bg-gradient-to-r from-amber-500 to-orange-500 text-white text-sm font-black shadow-md active:scale-95 transition-transform"
      >
        <Download className="w-4 h-4" />
        Install
      </button>
    </div>
  );

  return (
    <>
      {variant === 'card' ? (
        <div className={`rounded-2xl border-2 border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50 p-3.5 ${className}`}>{body}</div>
      ) : (
        <div
          className={`fixed inset-x-3 z-50 sm:left-auto sm:right-6 sm:w-[400px] ${
            aboveBottomNav ? 'bottom-[calc(4.75rem+env(safe-area-inset-bottom))] sm:bottom-6' : 'bottom-[calc(1rem+env(safe-area-inset-bottom))]'
          } animate-in slide-in-from-bottom-4 fade-in duration-300`}
          role="region"
          aria-label="Install app"
        >
          <div className="relative rounded-3xl border-2 border-amber-300 bg-white/95 backdrop-blur-md p-3.5 pr-9 shadow-xl shadow-amber-900/15">
            {body}
            <button
              onClick={handleDismiss}
              className="absolute top-1.5 right-1.5 p-1.5 rounded-full text-stone-400 hover:text-stone-700 hover:bg-stone-100"
              aria-label="Not now"
              title="Not now"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
      {showSteps && <InstructionsSheet platform={platform} onClose={() => setShowSteps(false)} />}
    </>
  );
};
