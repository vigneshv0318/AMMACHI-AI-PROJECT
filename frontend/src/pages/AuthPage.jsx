import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, KeyRound, User, ArrowRight, AlertCircle, Globe, ShieldCheck, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { authService } from '../services/authService';
import { AmmachiMascot } from '../components/common/AmmachiMascot';
import { InstallPrompt } from '../components/common/InstallPrompt';

export const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [selectedLang, setSelectedLang] = useState('Tamil');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [googleClientId, setGoogleClientId] = useState('');
  const googleBtnRef = useRef(null);

  const { login, signup, googleLogin } = useAuth();
  const { setLanguage } = useLanguage();
  const navigate = useNavigate();

  // Load Google Client ID & GIS SDK
  useEffect(() => {
    let isMounted = true;
    const initGoogleAuth = async () => {
      try {
        const config = await authService.getAuthConfig();
        if (config?.google_client_id && isMounted) {
          setGoogleClientId(config.google_client_id);
          
          if (!window.google) {
            const script = document.createElement('script');
            script.src = 'https://accounts.google.com/gsi/client';
            script.async = true;
            script.defer = true;
            script.onload = () => {
              if (window.google && googleBtnRef.current && isMounted) {
                renderGoogleButton(config.google_client_id);
              }
            };
            document.body.appendChild(script);
          } else if (googleBtnRef.current && isMounted) {
            renderGoogleButton(config.google_client_id);
          }
        }
      } catch (err) {
        console.warn('Could not fetch Google auth config:', err);
      }
    };

    const renderGoogleButton = (clientId) => {
      try {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: handleGoogleCallback,
          auto_select: false,
        });
        if (googleBtnRef.current) {
          googleBtnRef.current.innerHTML = '';
          window.google.accounts.id.renderButton(googleBtnRef.current, {
            theme: 'outline',
            size: 'large',
            width: '100%',
            text: 'continue_with',
            shape: 'pill',
          });
        }
      } catch (e) {
        console.error('Google button render error:', e);
      }
    };

    initGoogleAuth();
    return () => { isMounted = false; };
  }, []);

  const handleGoogleCallback = async (response) => {
    if (!response?.credential) return;
    setError('');
    setLoading(true);
    try {
      await googleLogin(response.credential);
      navigate('/');
    } catch (err) {
      console.error('Google auth error:', err);
      const msg = err.response?.data?.detail || 'Google authentication failed. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  // Demo Google Sign-In helper (bypasses Google Cloud Console setup requirement for instant local testing)
  const handleDemoGoogleAuth = async () => {
    setError('');
    setLoading(true);
    try {
      const payload = {
        sub: "google_10982736451",
        email: "soloistvicky03@gmail.com",
        name: "Vicky (Google User)"
      };
      // Construct URL-safe Base64 token payload
      const payloadB64 = btoa(JSON.stringify(payload));
      const simulatedToken = `eyJhbGciOiJIUzI1NiJ9.${payloadB64}.signature`;

      await googleLogin(simulatedToken);
      navigate('/');
    } catch (err) {
      console.error('Demo Google Auth error:', err);
      const msg = err.response?.data?.detail || 'Google authentication failed.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        await login(username, password);
      } else {
        await signup(username, password, selectedLang);
        setLanguage(selectedLang);
      }
      navigate('/');
    } catch (err) {
      console.error('Auth error:', err);
      const msg = err.response?.data?.detail || (isLogin ? 'Invalid username or password.' : 'Signup failed. Please try again.');
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = async () => {
    setLoading(true);
    try {
      await login('student', 'password123');
      navigate('/');
    } catch (err) {
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex flex-col items-center justify-center gap-4 py-6 px-4">
      <div className="w-full max-w-md bg-white border-2 border-amber-200/80 rounded-3xl p-6 sm:p-8 shadow-xl shadow-amber-500/5">
        {/* Header Mascot */}
        <div className="text-center mb-6">
          <AmmachiMascot size="lg" className="mb-3" />
          <h1 className="text-2xl sm:text-3xl font-black text-amber-950 tracking-tight">
            {isLogin ? "Welcome Back, Kanna!" : "Join Ammachi's Class!"}
          </h1>
          <p className="text-sm font-medium text-stone-600 mt-1">
            {isLogin ? "Your AI grandmother is waiting to teach you!" : "Learn native Indian languages with joyful AI guidance."}
          </p>
        </div>

        {/* Google OAuth Section */}
        <div className="mb-6 space-y-3">
          {/* Render Google GIS Button Container */}
          <div ref={googleBtnRef} className="w-full flex justify-center min-h-[44px]">
            <button
              type="button"
              onClick={handleDemoGoogleAuth}
              className="w-full py-3 px-4 bg-white border-2 border-stone-200 hover:border-amber-400 rounded-full flex items-center justify-center gap-3 text-stone-700 font-bold text-sm shadow-sm transition-all hover:bg-stone-50"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
              </svg>
              <span>Continue with Google</span>
            </button>
          </div>

          {/* Fallback direct Google test button if Google Cloud Console Client ID displays error */}
          <div className="text-center">
            <button
              type="button"
              onClick={handleDemoGoogleAuth}
              className="text-[11px] font-bold text-amber-800 hover:text-amber-950 underline decoration-amber-300 underline-offset-2"
            >
              ⚡ Click here to Test Google Sign-In without Cloud Console setup
            </button>
          </div>

          <div className="relative flex items-center justify-center pt-1">
            <div className="border-t border-stone-200 w-full" />
            <span className="bg-white px-3 text-xs font-bold text-stone-400 uppercase tracking-wider absolute">
              or use username
            </span>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-amber-100/70 p-1 rounded-2xl mb-6 border border-amber-200">
          <button
            type="button"
            onClick={() => { setIsLogin(true); setError(''); }}
            className={`flex-1 py-2.5 rounded-xl font-bold text-sm transition-all ${
              isLogin ? 'bg-white text-amber-900 shadow-sm' : 'text-stone-600 hover:text-stone-900'
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => { setIsLogin(false); setError(''); }}
            className={`flex-1 py-2.5 rounded-xl font-bold text-sm transition-all ${
              !isLogin ? 'bg-white text-amber-900 shadow-sm' : 'text-stone-600 hover:text-stone-900'
            }`}
          >
            New Student
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 p-3.5 bg-red-50 border border-red-200 rounded-2xl flex items-center gap-2 text-red-700 text-sm font-semibold">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-stone-700 uppercase tracking-wider mb-1.5">
              Username
            </label>
            <div className="relative">
              <User className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-amber-600" />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g. kanna_learns"
                className="w-full pl-11 pr-4 py-3 bg-amber-50/50 border border-amber-200 rounded-2xl text-stone-800 placeholder-stone-400 font-medium focus:outline-none focus:ring-2 focus:ring-amber-400 focus:bg-white transition-all text-base"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-stone-700 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <div className="relative">
              <KeyRound className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-amber-600" />
              <input
                type={showPassword ? 'text' : 'password'}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                autoComplete={isLogin ? 'current-password' : 'new-password'}
                className="w-full pl-11 pr-12 py-3 bg-amber-50/50 border border-amber-200 rounded-2xl text-stone-800 placeholder-stone-400 font-medium focus:outline-none focus:ring-2 focus:ring-amber-400 focus:bg-white transition-all text-base"
              />
              <button
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                title={showPassword ? 'Hide password' : 'Show password'}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full text-amber-700 hover:bg-amber-100 hover:text-amber-900 focus:outline-none focus:ring-2 focus:ring-amber-400 transition-colors"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {!isLogin && (
            <div>
              <label className="block text-xs font-bold text-stone-700 uppercase tracking-wider mb-1.5">
                Primary Native Language
              </label>
              <select
                value={selectedLang}
                onChange={(e) => setSelectedLang(e.target.value)}
                className="w-full px-4 py-3 bg-amber-50/50 border border-amber-200 rounded-2xl text-stone-800 font-semibold focus:outline-none focus:ring-2 focus:ring-amber-400 focus:bg-white transition-all text-base"
              >
                <option value="Tamil">Tamil (தமிழ்)</option>
                <option value="Telugu">Telugu (తెలుగు)</option>
                <option value="Hindi">Hindi (हिन्दी)</option>
              </select>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary mt-2"
          >
            <span>{loading ? "Connecting to Ammachi..." : (isLogin ? "Enter Class 🚀" : "Create Account ✨")}</span>
          </button>
        </form>

        {/* Quick Demo Student shortcut */}
        <div className="mt-6 pt-4 border-t border-amber-100 flex flex-col items-center gap-3">
          <button
            type="button"
            onClick={handleQuickDemo}
            className="text-xs font-bold text-amber-800 hover:text-amber-950 underline underline-offset-4 flex items-center gap-1 transition-colors"
          >
            <span>⚡ Quick Demo: Enter as Student</span>
            <ArrowRight className="w-3 h-3" />
          </button>
        </div>
      </div>
      <InstallPrompt variant="card" className="w-full max-w-md" />
    </div>
  );
};
