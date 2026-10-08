import React, { useState } from 'react';

export const AmmachiMascot = ({ size = 'md', className = '', speaking = false }) => {
  const [imgFailed, setImgFailed] = useState(false);
  const sizeClasses = {
    xs: 'w-10 h-10',
    sm: 'w-12 h-12 sm:w-14 sm:h-14',
    md: 'w-20 h-20',
    lg: 'w-24 h-24 sm:w-28 sm:h-28',
    xl: 'w-32 h-32 sm:w-36 sm:h-36'
  };

  return (
    <div
      className={`relative inline-flex shrink-0 items-center justify-center rounded-full bg-white p-[3px] shadow-md shadow-orange-500/20 ${
        speaking ? 'ring-4 ring-amber-300 animate-pulse' : ''
      } ${className}`}
    >
      <div className={`flex items-center justify-center rounded-full overflow-hidden ${sizeClasses[size] || sizeClasses.md}`}>
        {imgFailed ? (
          <span className="flex w-full h-full items-center justify-center bg-gradient-to-br from-amber-300 to-orange-400 text-3xl leading-none" role="img" aria-label="Ammachi Mascot">👵</span>
        ) : (
          <img
            src="/logo/ammachi.svg"
            alt="Ammachi Mascot"
            draggable="false"
            onError={() => setImgFailed(true)}
            className="w-full h-full object-cover select-none"
          />
        )}
      </div>
      {speaking && (
        <span className="absolute -top-1 -right-1 flex h-4 w-4">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-4 w-4 bg-orange-500"></span>
        </span>
      )}
    </div>
  );
};
