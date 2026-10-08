import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from './Navbar';
import { BottomNav } from './BottomNav';
import { WifiOff } from 'lucide-react';

export const Layout = () => {
  const [isOffline, setIsOffline] = useState(!navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-warmbg text-stone-800 pb-20 sm:pb-8">
      {isOffline && (
        <div className="bg-amber-600 text-white text-xs font-bold py-1.5 px-4 text-center flex items-center justify-center gap-2">
          <WifiOff className="w-4 h-4" />
          <span>You are offline. Static learning lessons are available!</span>
        </div>
      )}
      <Navbar />
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-4 sm:py-8">
        <Outlet />
      </main>
      <BottomNav />
    </div>
  );
};
