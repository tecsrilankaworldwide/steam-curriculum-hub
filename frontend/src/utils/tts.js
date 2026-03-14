// Text-to-Speech utility for Sinhala STEAM Education Hub
// Uses Browser Built-in TTS (FREE - No API key needed!)
// Perfect for Sinhala and English voice reading

// Split long text into chunks (Google TTS has ~200 char limit)
function splitTextIntoChunks(text, maxLength = 180) {
  const chunks = [];
  const sentences = text.split(/(?<=[.!?။।])\s+|(?<=\n)/);
  let current = '';
  
  for (const sentence of sentences) {
    if ((current + sentence).length > maxLength) {
      if (current.trim()) chunks.push(current.trim());
      // If single sentence is too long, split by words
      if (sentence.length > maxLength) {
        const words = sentence.split(/\s+/);
        current = '';
        for (const word of words) {
          if ((current + ' ' + word).length > maxLength) {
            if (current.trim()) chunks.push(current.trim());
            current = word;
          } else {
            current = current ? current + ' ' + word : word;
          }
        }
      } else {
        current = sentence;
      }
    } else {
      current = current ? current + ' ' + sentence : sentence;
    }
  }
  if (current.trim()) chunks.push(current.trim());
  return chunks;
}

// Play audio from Google Translate TTS
async function playGoogleTTS(text, langCode) {
  const googleLang = GOOGLE_TTS_LANG[langCode] || langCode.split('-')[0];
  const chunks = splitTextIntoChunks(text);
  
  for (let i = 0; i < chunks.length; i++) {
    const chunk = chunks[i];
    const encodedText = encodeURIComponent(chunk);
    const url = `https://translate.google.com/translate_tts?ie=UTF-8&q=${encodedText}&tl=${googleLang}&client=tw-ob`;
    
    try {
      const audio = new Audio(url);
      audio.crossOrigin = "anonymous";
      
      await new Promise((resolve, reject) => {
        audio.onended = resolve;
        audio.onerror = reject;
        audio.oncanplaythrough = () => audio.play().catch(reject);
        
        // Timeout after 10 seconds per chunk
        setTimeout(() => reject(new Error('timeout')), 10000);
      });
    } catch (e) {
      console.warn(`Google TTS chunk ${i + 1} failed:`, e.message);
      // Try browser TTS for this chunk
      await playBrowserTTSChunk(chunk, langCode);
    }
  }
}

// Browser TTS for a single chunk
function playBrowserTTSChunk(text, langCode) {
  return new Promise((resolve) => {
    if (!window.speechSynthesis) {
      resolve();
      return;
    }
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = langCode;
    utterance.rate = 0.85;
    utterance.pitch = 1;
    
    const voices = window.speechSynthesis.getVoices();
    const voice = voices.find(v => v.lang === langCode) || 
                  voices.find(v => v.lang.startsWith(langCode.split('-')[0]));
    
    if (voice) {
      utterance.voice = voice;
    }
    
    utterance.onend = resolve;
    utterance.onerror = resolve;
    
    window.speechSynthesis.speak(utterance);
  });
}

// Main speak function - Uses Browser TTS (FREE!)
export const speak = async (text, langCode, onEnd) => {
  // Cancel any ongoing speech
  window.speechSynthesis.cancel();
  
  if (!text || text.trim().length < 2) {
    console.warn('No text to speak');
    if (onEnd) onEnd();
    return;
  }
  
  // Clean the text - remove markdown formatting
  const cleanText = text
    .replace(/#{1,6}\s+/g, '') // Remove markdown headers
    .replace(/\*\*(.*?)\*\*/g, '$1') // Remove bold
    .replace(/\*(.*?)\*/g, '$1') // Remove italic
    .replace(/`(.*?)`/g, '$1') // Remove code
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Remove links, keep text
    .replace(/^[-*+]\s+/gm, '') // Remove list bullets
    .trim();
  
  console.log(`🔊 Speaking in ${langCode}: "${cleanText.substring(0, 60)}..."`);
  
  try {
    // Use Browser TTS - FREE and works great for Sinhala!
    const chunks = splitTextIntoChunks(cleanText);
    for (const chunk of chunks) {
      await playBrowserTTSChunk(chunk, langCode);
    }
    console.log('✅ Browser TTS completed');
  } catch (error) {
    console.error('❌ TTS failed:', error.message);
  }
  
  if (onEnd) onEnd();
};

export const stopSpeaking = () => {
  window.speechSynthesis.cancel();
  // Also stop any audio elements
  document.querySelectorAll('audio').forEach(a => {
    a.pause();
    a.currentTime = 0;
  });
};

// Language configurations - FOCUSED ON SRI LANKA
export const LANGUAGES = [
  { code: 'si-LK', name: 'Sinhala', nativeName: 'සිංහල', rtl: false, flag: '🇱🇰' },
  { code: 'en-US', name: 'English', nativeName: 'English', rtl: false, flag: '🇬🇧' },
  // Tamil ready when budget approved:
  // { code: 'ta-IN', name: 'Tamil', nativeName: 'தமிழ்', rtl: false, flag: '🇱🇰' },
];

export const getLanguageName = (code) => {
  const lang = LANGUAGES.find(l => l.code === code);
  return lang ? `${lang.nativeName} / ${lang.name}` : code;
};

export const isRTL = (langCode) => {
  const lang = LANGUAGES.find(l => l.code === langCode);
  return lang ? lang.rtl : false;
};
