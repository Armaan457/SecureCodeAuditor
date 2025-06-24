import { useEffect, useState } from 'react';

interface GlitchTextProps {
  text: string;
  className?: string;
}

export function GlitchText({ text, className = '' }: GlitchTextProps) {
  const [isGlitching, setIsGlitching] = useState(false);

  useEffect(() => {
    const glitchInterval = setInterval(() => {
      setIsGlitching(true);
      setTimeout(() => setIsGlitching(false), 150);
    }, 3000);

    return () => clearInterval(glitchInterval);
  }, []);

  return (
    <span 
      className={`
        relative inline-block
        ${className}
        ${isGlitching ? 'glitch' : ''}
      `} 
      data-text={text}
    >
      {text}
      {isGlitching && (
        <>
          <span className="absolute inset-0 text-green-500 glitch-1" aria-hidden="true">{text}</span>
          <span className="absolute inset-0 text-red-500 glitch-2" aria-hidden="true">{text}</span>
        </>
      )}
    </span>
  );
}