import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Camera, X, RefreshCw, Loader2, AlertTriangle } from 'lucide-react';

const describeCameraError = (err) => {
  if (!window.isSecureContext) {
    return 'The camera only works on https:// or http://localhost. Use "Upload Photo" instead.';
  }
  switch (err?.name) {
    case 'NotAllowedError':
    case 'SecurityError':
      return 'Camera permission was denied. Allow camera access in your browser settings and try again.';
    case 'NotFoundError':
    case 'OverconstrainedError':
      return 'No camera was found on this device. Use "Upload Photo" instead.';
    case 'NotReadableError':
      return 'The camera is being used by another app. Close it and try again.';
    default:
      return 'Could not start the camera. Use "Upload Photo" instead.';
  }
};

/**
 * Full-screen live camera. Calls onCapture(File) with a JPEG snapshot of the current frame.
 */
export const CameraCapture = ({ targetLetter, onCapture, onClose, onFallbackUpload }) => {
  const videoRef = useRef(null);
  const guideRef = useRef(null);
  const streamRef = useRef(null);
  const [facingMode, setFacingMode] = useState('environment');
  const [hasMultipleCameras, setHasMultipleCameras] = useState(false);
  const [starting, setStarting] = useState(true);
  const [error, setError] = useState('');
  const [flash, setFlash] = useState(false);

  const stopStream = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
  }, []);

  useEffect(() => {
    let cancelled = false;

    const start = async () => {
      setStarting(true);
      setError('');
      stopStream();

      if (!navigator.mediaDevices?.getUserMedia) {
        setError(describeCameraError(null));
        setStarting(false);
        return;
      }

      try {
        let stream;
        try {
          stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: { ideal: facingMode }, width: { ideal: 1920 }, height: { ideal: 1080 } },
            audio: false,
          });
        } catch (firstErr) {
          if (firstErr?.name !== 'OverconstrainedError') throw firstErr;
          stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        }

        if (cancelled) {
          stream.getTracks().forEach((track) => track.stop());
          return;
        }
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          await videoRef.current.play().catch(() => {});
        }

        const devices = await navigator.mediaDevices.enumerateDevices();
        if (!cancelled) {
          setHasMultipleCameras(devices.filter((d) => d.kind === 'videoinput').length > 1);
        }
      } catch (err) {
        console.error('Camera error:', err);
        if (!cancelled) setError(describeCameraError(err));
      } finally {
        if (!cancelled) setStarting(false);
      }
    };

    start();
    return () => {
      cancelled = true;
      stopStream();
    };
  }, [facingMode, stopStream]);

  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  // Map the on-screen guide box to the camera's own pixel coordinates.
  // The video uses object-cover, so it is scaled up and centered (and mirrored for the front camera).
  const getGuideCropRect = (video) => {
    const box = guideRef.current?.getBoundingClientRect();
    const view = video.getBoundingClientRect();
    const srcW = video.videoWidth;
    const srcH = video.videoHeight;
    if (!box || !view.width || !view.height) return { sx: 0, sy: 0, sw: srcW, sh: srcH };

    const scale = Math.max(view.width / srcW, view.height / srcH);
    const offsetX = (view.width - srcW * scale) / 2;
    const offsetY = (view.height - srcH * scale) / 2;

    let boxLeft = box.left - view.left;
    const boxTop = box.top - view.top;
    if (facingMode === 'user') boxLeft = view.width - (boxLeft + box.width);

    const sx = Math.max(0, (boxLeft - offsetX) / scale);
    const sy = Math.max(0, (boxTop - offsetY) / scale);
    const sw = Math.min(srcW - sx, box.width / scale);
    const sh = Math.min(srcH - sy, box.height / scale);
    return { sx, sy, sw, sh };
  };

  const handleCapture = () => {
    const video = videoRef.current;
    if (!video || !video.videoWidth) return;

    // Only the area inside the guide box is kept and sent for OCR
    const { sx, sy, sw, sh } = getGuideCropRect(video);
    const canvas = document.createElement('canvas');
    canvas.width = Math.round(sw);
    canvas.height = Math.round(sh);
    const ctx = canvas.getContext('2d');
    // The front camera preview is mirrored for the user, but the saved photo must not be
    ctx.drawImage(video, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);

    setFlash(true);
    setTimeout(() => setFlash(false), 150);

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setError('Could not capture the photo. Please try again.');
          return;
        }
        stopStream();
        onCapture(new File([blob], `handwriting-${Date.now()}.jpg`, { type: 'image/jpeg' }));
      },
      'image/jpeg',
      0.92
    );
  };

  const isMirrored = facingMode === 'user';

  return (
    <div className="fixed inset-0 z-50 bg-black flex flex-col" role="dialog" aria-modal="true" aria-label="Take a photo">
      {/* Top bar */}
      <div className="flex items-center justify-between px-4 py-3 text-white">
        <button onClick={onClose} className="p-2 rounded-full bg-white/10 hover:bg-white/20" aria-label="Close camera">
          <X className="w-6 h-6" />
        </button>
        {targetLetter && (
          <div className="text-center">
            <p className="text-[11px] font-bold uppercase tracking-wider text-white/70">Writing</p>
            <p className="text-3xl font-black leading-none">{targetLetter}</p>
          </div>
        )}
        {hasMultipleCameras && !error ? (
          <button
            onClick={() => setFacingMode((m) => (m === 'environment' ? 'user' : 'environment'))}
            className="p-2 rounded-full bg-white/10 hover:bg-white/20"
            aria-label="Switch camera"
          >
            <RefreshCw className="w-6 h-6" />
          </button>
        ) : (
          <span className="w-10" />
        )}
      </div>

      {/* Viewfinder */}
      <div className="relative flex-1 overflow-hidden flex items-center justify-center">
        <video
          ref={videoRef}
          playsInline
          muted
          autoPlay
          className={`w-full h-full object-cover ${isMirrored ? '-scale-x-100' : ''}`}
        />

        {!error && !starting && (
          <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
            <div
              ref={guideRef}
              className="w-64 h-64 max-w-[70vw] max-h-[70vw] rounded-3xl border-4 border-amber-400/90 shadow-[0_0_0_9999px_rgba(0,0,0,0.6)]"
            />
            <p className="mt-4 px-3 py-1.5 rounded-full bg-black/60 text-white text-sm font-bold">
              Only what's inside the box will be checked
            </p>
          </div>
        )}

        {starting && !error && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-white gap-3">
            <Loader2 className="w-10 h-10 animate-spin text-amber-400" />
            <p className="font-bold">Starting camera...</p>
          </div>
        )}

        {error && (
          <div className="absolute inset-0 flex items-center justify-center p-6">
            <div className="bg-white rounded-2xl p-6 max-w-sm w-full text-center space-y-4">
              <AlertTriangle className="w-10 h-10 text-amber-500 mx-auto" />
              <p className="font-bold text-stone-700 text-sm">{error}</p>
              <div className="flex gap-2">
                <button
                  onClick={onClose}
                  className="flex-1 py-2.5 rounded-xl border-2 border-stone-200 font-black text-stone-700"
                >
                  Close
                </button>
                {onFallbackUpload && (
                  <button
                    onClick={onFallbackUpload}
                    className="flex-1 py-2.5 rounded-xl bg-amber-500 text-white font-black"
                  >
                    Upload Photo
                  </button>
                )}
              </div>
            </div>
          </div>
        )}

        {flash && <div className="absolute inset-0 bg-white" />}
      </div>

      {/* Shutter */}
      <div className="py-6 flex items-center justify-center">
        <button
          onClick={handleCapture}
          disabled={starting || !!error}
          className="w-20 h-20 rounded-full bg-white border-[6px] border-amber-400 flex items-center justify-center shadow-lg active:scale-95 transition-transform disabled:opacity-40"
          aria-label="Take photo"
        >
          <Camera className="w-8 h-8 text-amber-600" />
        </button>
      </div>
    </div>
  );
};
