// Shared state for the "Install app" prompt (Chrome / Edge / Samsung Internet on Android & desktop).
let deferredPrompt = null;
const listeners = new Set();

const notify = () => listeners.forEach((fn) => fn());

export const captureInstallPrompt = () => {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault(); // keep it for our own button instead of the browser's mini bar
    deferredPrompt = e;
    notify();
  });
  window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    notify();
  });
};

export const subscribeInstall = (fn) => {
  listeners.add(fn);
  return () => listeners.delete(fn);
};

export const canPromptInstall = () => !!deferredPrompt;

/** Shows the native install dialog. Resolves to 'accepted', 'dismissed' or 'unavailable'. */
export const promptInstall = async () => {
  if (!deferredPrompt) return 'unavailable';
  const prompt = deferredPrompt;
  deferredPrompt = null; // a prompt event can only be used once
  notify();
  prompt.prompt();
  const { outcome } = await prompt.userChoice;
  return outcome;
};

export const isStandalone = () =>
  window.matchMedia?.('(display-mode: standalone)').matches || window.navigator.standalone === true;

export const getPlatform = () => {
  const ua = navigator.userAgent || '';
  const isIOS = /iPad|iPhone|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (isIOS) {
    // On iOS only Safari can add to the home screen in older versions; newer iOS allows Chrome too
    const inAppBrowser = /FBAN|FBAV|Instagram|Line\/|WhatsApp/i.test(ua);
    return inAppBrowser ? 'ios-inapp' : 'ios';
  }
  if (/Android/i.test(ua)) return 'android';
  return 'desktop';
};
