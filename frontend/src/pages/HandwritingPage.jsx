import React, { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Upload, Camera, CheckCircle, XCircle, Loader2, RotateCcw, Send } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { handwritingService } from '../services/handwritingService';
import { AmmachiMascot } from '../components/common/AmmachiMascot';
import { CameraCapture } from '../components/writing/CameraCapture';

const MAX_IMAGE_DIMENSION = 1600;
const MAX_UPLOAD_BYTES = 5 * 1024 * 1024;

// Shrink large phone photos so they stay under the backend's 5MB limit and upload quickly
const prepareImage = async (file) => {
  if (file.size <= MAX_UPLOAD_BYTES / 2) return file;
  try {
    const bitmap = await createImageBitmap(file, { imageOrientation: 'from-image' });
    const scale = Math.min(1, MAX_IMAGE_DIMENSION / Math.max(bitmap.width, bitmap.height));
    const canvas = document.createElement('canvas');
    canvas.width = Math.round(bitmap.width * scale);
    canvas.height = Math.round(bitmap.height * scale);
    canvas.getContext('2d').drawImage(bitmap, 0, 0, canvas.width, canvas.height);
    bitmap.close?.();
    const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', 0.9));
    return blob ? new File([blob], file.name.replace(/\.\w+$/, '') + '.jpg', { type: 'image/jpeg' }) : file;
  } catch {
    return file;
  }
};

const LANGUAGES = [
  { code: 'Tamil', name: 'Tamil', flag: '🇮🇳' },
  { code: 'Hindi', name: 'Hindi', flag: '🇮🇳' },
  { code: 'Telugu', name: 'Telugu', flag: '🇮🇳' },
  { code: 'Malayalam', name: 'Malayalam', flag: '🇮🇳' }
];

export const HandwritingPage = () => {
  const navigate = useNavigate();
  const [selectedLang, setSelectedLang] = useState('Tamil');
  const [letters, setLetters] = useState([]);
  const [selectedLetter, setSelectedLetter] = useState(null);
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [cameraOpen, setCameraOpen] = useState(false);
  const [photo, setPhoto] = useState(null); // { file, url }

  const fileInputRef = useRef(null);

  const clearPhoto = () => {
    setPhoto((prev) => {
      if (prev?.url) URL.revokeObjectURL(prev.url);
      return null;
    });
  };

  // Release the preview URL when leaving the page
  const photoRef = useRef(null);
  photoRef.current = photo;
  useEffect(() => () => {
    if (photoRef.current?.url) URL.revokeObjectURL(photoRef.current.url);
  }, []);

  // Fetch letters when language changes
  useEffect(() => {
    const fetchLetters = async () => {
      setLoading(true);
      setError('');
      setResult(null);
      setSelectedLetter(null);
      clearPhoto();
      try {
        const data = await handwritingService.getLetters(selectedLang);
        setLetters(data.letters || []);
      } catch (err) {
        setError('Failed to load letters: ' + err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchLetters();
  }, [selectedLang]);

  const setPhotoFile = (file) => {
    clearPhoto();
    setPhoto({ file, url: URL.createObjectURL(file) });
    setResult(null);
    setError('');
  };

  const handleFileUpload = (event) => {
    const file = event.target.files?.[0];
    // Reset input so same file can be selected again
    event.target.value = '';
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      setError('Please choose an image file (JPG or PNG).');
      return;
    }
    setPhotoFile(file);
  };

  const handleCameraCapture = (file) => {
    setCameraOpen(false);
    setPhotoFile(file);
  };

  const openUploadPicker = () => {
    setCameraOpen(false);
    fileInputRef.current?.click();
  };

  const handleSubmit = async () => {
    if (!selectedLetter) {
      setError('Please select a letter to write first.');
      return;
    }
    if (!photo) return;

    setEvaluating(true);
    setError('');
    setResult(null);

    try {
      const imageFile = await prepareImage(photo.file);
      if (imageFile.size > MAX_UPLOAD_BYTES) {
        throw new Error('This photo is too large (max 5MB). Please take a new photo.');
      }
      const evaluation = await handwritingService.evaluateHandwriting(selectedLetter.id, imageFile);
      setResult(evaluation);
    } catch (err) {
      setError(err.message);
    } finally {
      setEvaluating(false);
    }
  };

  const retryLetter = () => {
    clearPhoto();
    setResult(null);
    setError('');
  };

  return (
    <div className="flex justify-center">
      <div className="max-w-md w-full space-y-4 sm:space-y-6">
        <button onClick={() => navigate('/')} className="flex items-center text-stone-500 font-bold text-sm hover:text-stone-800 transition-colors">
          <ArrowLeft className="w-4 h-4 mr-1" /> Back to Dashboard
        </button>

        <div className="bg-white rounded-3xl p-4 sm:p-6 shadow-lg shadow-amber-500/10 border-2 border-amber-200">
          <div className="flex flex-col items-center mb-6 text-center">
            <AmmachiMascot size="md" className="mb-3" />
            <h1 className="text-2xl font-black text-amber-950 tracking-tight">Handwriting Practice</h1>
            <p className="text-sm font-semibold text-stone-500 mt-1">Write letters in your notebook and let Ammachi check them!</p>
          </div>

          <div className="space-y-6">
            {/* Language Selection */}
            <div>
              <label className="block text-xs font-black text-stone-600 uppercase mb-2">Language</label>
              <div className="grid grid-cols-2 min-[400px]:grid-cols-4 gap-2">
                {LANGUAGES.map(lang => (
                  <button
                    key={lang.code}
                    onClick={() => setSelectedLang(lang.code)}
                    className={`px-2 py-2.5 rounded-xl border-2 text-sm font-bold transition-all active:scale-95 ${
                      selectedLang === lang.code
                        ? 'border-amber-500 bg-amber-50 text-amber-900'
                        : 'border-stone-200 bg-white text-stone-600 hover:border-amber-200'
                    }`}
                  >
                    {lang.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Letter Selection */}
            <div>
              <label className="block text-xs font-black text-stone-600 uppercase mb-2">Select a Letter to Practice</label>
              {loading ? (
                <div className="flex justify-center py-4"><Loader2 className="animate-spin text-amber-500" /></div>
              ) : letters.length === 0 ? (
                <p className="text-sm text-stone-500 italic py-2">No letters available for this language yet.</p>
              ) : (
                <div className="grid grid-cols-4 min-[400px]:grid-cols-5 gap-2">
                  {letters.map(letter => (
                    <button
                      key={letter.id}
                      onClick={() => {
                        setSelectedLetter(letter);
                        setResult(null);
                        setError('');
                        clearPhoto();
                      }}
                      className={`text-2xl aspect-square flex items-center justify-center rounded-xl border-2 font-black transition-all active:scale-95 ${
                        selectedLetter?.id === letter.id
                          ? 'border-amber-500 bg-amber-50 text-amber-900 transform scale-105'
                          : 'border-stone-200 bg-white text-stone-600 hover:border-amber-200'
                      }`}
                    >
                      {letter.character}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-rose-50 border border-rose-200 text-rose-700 p-3 rounded-xl text-sm font-bold">
                {error}
              </div>
            )}

            <input
              type="file"
              accept="image/*"
              className="hidden"
              ref={fileInputRef}
              onChange={handleFileUpload}
            />

            {/* Action Area: choose camera or upload */}
            {selectedLetter && !photo && !result && !evaluating && (
              <div className="bg-amber-100 p-6 rounded-2xl border-2 border-amber-300 text-center animate-in fade-in zoom-in-95">
                <p className="text-sm font-black text-amber-900 mb-2 uppercase tracking-wide">Write this letter clearly:</p>
                <div className="text-6xl font-black text-amber-950 mb-2 drop-shadow-sm">
                  {selectedLetter.character}
                </div>
                <p className="text-xs font-semibold text-amber-800 mb-5">
                  Write it big and dark on plain paper, then take a photo in good light.
                </p>

                <div className="space-y-2">
                  <button
                    onClick={() => setCameraOpen(true)}
                    className="w-full py-3.5 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-xl font-black text-lg shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all flex items-center justify-center gap-2"
                  >
                    <Camera className="w-5 h-5" />
                    Open Camera
                  </button>
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="w-full py-3 bg-white text-amber-900 border-2 border-amber-300 rounded-xl font-black text-base hover:bg-amber-50 transition-colors flex items-center justify-center gap-2"
                  >
                    <Upload className="w-5 h-5" />
                    Upload Photo
                  </button>
                </div>
              </div>
            )}

            {/* Preview: retake or submit */}
            {selectedLetter && photo && !result && (
              <div className="bg-amber-50 p-4 rounded-2xl border-2 border-amber-300 text-center animate-in fade-in zoom-in-95 space-y-4">
                <div className="flex items-center justify-between px-1">
                  <p className="text-sm font-black text-amber-900 uppercase tracking-wide">Check your photo</p>
                  <span className="text-3xl font-black text-amber-950">{selectedLetter.character}</span>
                </div>
                <div className="relative rounded-xl overflow-hidden border-2 border-amber-200 bg-stone-100">
                  <img src={photo.url} alt="Your handwriting" className="w-full max-h-80 object-contain" />
                  {evaluating && (
                    <div className="absolute inset-0 bg-white/75 flex flex-col items-center justify-center">
                      <Loader2 className="w-10 h-10 animate-spin text-amber-500 mb-3" />
                      <p className="font-bold text-stone-700">Ammachi is reading your handwriting...</p>
                    </div>
                  )}
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => { clearPhoto(); setCameraOpen(true); }}
                    disabled={evaluating}
                    className="py-3 bg-white text-stone-800 border-2 border-stone-200 rounded-xl font-black hover:bg-stone-50 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    <RotateCcw className="w-4 h-4" />
                    Retake
                  </button>
                  <button
                    onClick={handleSubmit}
                    disabled={evaluating}
                    className="py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-xl font-black shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-60"
                  >
                    {evaluating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                    {evaluating ? 'Checking...' : 'Check'}
                  </button>
                </div>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={evaluating}
                  className="text-xs font-bold text-amber-800 underline disabled:opacity-50"
                >
                  Choose a different photo
                </button>
              </div>
            )}

            {/* Result Area */}
            {result && !evaluating && (
              <div className={`p-6 rounded-2xl border-2 text-center animate-in zoom-in-95 ${
                result.status === 'correct' ? 'bg-emerald-50 border-emerald-300' : 
                result.status === 'incorrect' ? 'bg-rose-50 border-rose-300' :
                'bg-amber-50 border-amber-300'
              }`}>
                {result.status === 'correct' ? (
                  <CheckCircle className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
                ) : result.status === 'incorrect' ? (
                  <XCircle className="w-12 h-12 text-rose-500 mx-auto mb-3" />
                ) : (
                  <Camera className="w-12 h-12 text-amber-500 mx-auto mb-3" />
                )}
                
                <h3 className={`text-xl font-black mb-1 ${
                  result.status === 'correct' ? 'text-emerald-800' : 
                  result.status === 'incorrect' ? 'text-rose-800' :
                  'text-amber-800'
                }`}>
                  {result.status === 'correct' ? '✅ Sabash! Correct!' : 
                   result.status === 'incorrect' ? '❌ Try Again Kanna' : 
                   result.status === 'ocr_unavailable' ? '⚠️ Couldn\'t check the image' :
                   '📷 Couldn\'t recognize the letter'}
                </h3>
                
                <p className="font-bold text-stone-700 mb-4 text-sm">{result.feedback}</p>

                {photo && (
                  <div className="flex items-center justify-center gap-4 mb-4">
                    <img src={photo.url} alt="Your handwriting" className="w-24 h-24 object-cover rounded-xl border-2 border-white shadow" />
                    <div className="text-left text-sm font-bold text-stone-600 space-y-1">
                      <p>Target: <span className="text-2xl font-black text-stone-900 align-middle">{result.target}</span></p>
                      {result.detected && (
                        <p>Ammachi saw: <span className="text-2xl font-black text-stone-900 align-middle">{result.detected}</span></p>
                      )}
                    </div>
                  </div>
                )}

                {result.score !== null && result.score !== undefined && (
                  <div className="inline-block bg-white px-4 py-2 rounded-lg font-black text-amber-600 border border-stone-200 mb-6 shadow-sm">
                    Score: {result.score}
                  </div>
                )}

                <div className="space-y-2">
                  {result.status !== 'correct' && (
                    <button
                      onClick={() => { retryLetter(); setCameraOpen(true); }}
                      className="w-full py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-xl font-black text-base shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2"
                    >
                      <Camera className="w-5 h-5" />
                      Try This Letter Again
                    </button>
                  )}
                  <button
                    onClick={() => {
                      retryLetter();
                      setSelectedLetter(null);
                    }}
                    className="w-full py-3 bg-white text-stone-800 border-2 border-stone-200 rounded-xl font-black text-base hover:bg-stone-50 transition-colors"
                  >
                    Practice Another Letter
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {cameraOpen && (
        <CameraCapture
          targetLetter={selectedLetter?.character}
          onCapture={handleCameraCapture}
          onClose={() => setCameraOpen(false)}
          onFallbackUpload={openUploadPicker}
        />
      )}
    </div>
  );
};
