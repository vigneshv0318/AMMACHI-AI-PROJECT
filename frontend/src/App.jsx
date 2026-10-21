import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { AuthPage } from './pages/AuthPage';
import { DashboardPage } from './pages/DashboardPage';

import { SpeakingPage } from './pages/SpeakingPage';
import { CulturePage } from './pages/CulturePage';
import { ProgressPage } from './pages/ProgressPage';
import { ChallengePage } from './pages/ChallengePage';
import { HandwritingPage } from './pages/HandwritingPage';
import { ProfilePage } from './pages/ProfilePage';
import { LearnPathPage } from './pages/LearnPathPage';
import { LessonPlayerPage } from './pages/LessonPlayerPage';
import { LeaderboardPage } from './pages/LeaderboardPage';
import { QuestsPage } from './pages/QuestsPage';
import { ShopPage } from './pages/ShopPage';
import { LoadingScreen } from './components/common/LoadingScreen';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { useAuth } from './context/AuthContext';

function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <Routes>
      {/* Auth Route: Redirect to dashboard if already authenticated */}
      <Route
        path="/auth"
        element={user ? <Navigate to="/" replace /> : <AuthPage />}
      />

      {/* Main App Shell Layout (Protected Routes) */}
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<DashboardPage />} />

        <Route path="/speaking" element={<SpeakingPage />} />
        <Route path="/culture" element={<CulturePage />} />
        <Route path="/progress" element={<ProgressPage />} />
        <Route path="/challenge" element={<ChallengePage />} />
        <Route path="/challenge/:id" element={<ChallengePage />} />
        <Route path="/handwriting" element={<HandwritingPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/learn" element={<LearnPathPage />} />
        <Route path="/leaderboard" element={<LeaderboardPage />} />
        <Route path="/quests" element={<QuestsPage />} />
        <Route path="/shop" element={<ShopPage />} />
      </Route>

      {/* Lesson player: full-screen immersive (outside app shell) */}
      <Route
        path="/learn/lesson"
        element={
          <ProtectedRoute>
            <LessonPlayerPage />
          </ProtectedRoute>
        }
      />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
