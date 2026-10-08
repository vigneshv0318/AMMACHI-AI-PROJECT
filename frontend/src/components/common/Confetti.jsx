import confetti from 'canvas-confetti';

export const triggerCelebration = () => {
  try {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#F59E0B', '#EF4444', '#10B981', '#6366F1', '#EC4899', '#FBBF24']
    });
  } catch (e) {
    console.warn("Confetti error:", e);
  }
};
