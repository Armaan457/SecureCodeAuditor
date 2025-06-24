import { useEffect, useState } from 'react';

export function HackerLoader() {
  const [text, setText] = useState('Initializing System');
  const messages = [
    'Initializing System',
    'Establishing Secure Connection'
  ];

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      index = (index + 1) % messages.length;
      setText(messages[index]);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loader">
      <div className="loader-text">{text}<span className="cursor">_</span></div>
      <div className="loader-progress">
        <div className="progress-bar" />
      </div>
      <div className="loader-dots">
        <div className="dot"></div>
        <div className="dot"></div>
        <div className="dot"></div>
      </div>
    </div>
  );
}