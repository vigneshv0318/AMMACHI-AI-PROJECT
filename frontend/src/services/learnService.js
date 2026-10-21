import api from './api';

/**
 * Learn Path & Gamification API client — Duolingo-style features.
 * All endpoints are served by the FastAPI backend under /learn.
 */
export const learnService = {
  /** Full learning path with per-node progress for the current language */
  async getPath(language) {
    const q = language ? `?language=${encodeURIComponent(language)}` : '';
    const response = await api.get(`/learn/path${q}`);
    return response.data;
  },

  /** Node intro screen data (lesson no, XP, hearts) */
  async getNodePreview(nodeId) {
    const response = await api.get(`/learn/node/${nodeId}/preview`);
    return response.data;
  },

  /** Start a lesson attempt (generates/binds exercises) */
  async startAttempt(nodeId) {
    const response = await api.post(`/learn/node/${nodeId}/start`);
    return response.data;
  },

  /** Check one answer; server validates + handles hearts */
  async checkAnswer(attemptId, exerciseId, answer) {
    const response = await api.post(`/learn/attempt/${attemptId}/answer`, {
      exercise_id: exerciseId,
      answer,
    });
    return response.data;
  },

  /** Finish lesson: awards XP, stars, streak, quests */
  async completeAttempt(attemptId) {
    const response = await api.post(`/learn/attempt/${attemptId}/complete`);
    return response.data;
  },

  async quitAttempt(attemptId) {
    const response = await api.post(`/learn/attempt/${attemptId}/quit`);
    return response.data;
  },

  /** HUD counters: streak, gems, hearts, XP, quests */
  async getHud() {
    const response = await api.get('/learn/hud');
    return response.data;
  },

  /** Weekly league leaderboard */
  async getLeaderboard() {
    const response = await api.get('/learn/leaderboard');
    return response.data;
  },

  /** Daily quests + claim chest */
  async claimQuest(questType) {
    const response = await api.post(`/learn/quests/${questType}/claim`);
    return response.data;
  },

  /** Shop */
  async getShop() {
    const response = await api.get('/learn/shop');
    return response.data;
  },

  async purchase(itemId) {
    const response = await api.post('/learn/shop/purchase', { item_id: itemId });
    return response.data;
  },

  async setDailyGoal(goal) {
    const response = await api.post('/learn/goal', { daily_goal: goal });
    return response.data;
  },
};
