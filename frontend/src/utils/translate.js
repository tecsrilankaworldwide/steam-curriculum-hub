// Translation utility using MyMemory Translation API (Free, no API key needed)

const TRANSLATION_CACHE = new Map();

const LANGUAGE_MAP = {
  'en-US': 'en',
  'si-LK': 'si',
  'hi-IN': 'hi',
  'ar-SA': 'ar',
  'zh-CN': 'zh',
  'ja-JP': 'ja',
  'es-ES': 'es',
  'fr-FR': 'fr',
  'de-DE': 'de',
  'ru-RU': 'ru',
  'ko-KR': 'ko',
  'vi-VN': 'vi',
  'th-TH': 'th',
  'id-ID': 'id',
  'fil-PH': 'tl',
  'ta-IN': 'ta',
  'te-IN': 'te',
  'bn-IN': 'bn',
  'ur-PK': 'ur',
  'ne-NP': 'ne',
  'pa-IN': 'pa',
  'ps-AF': 'ps'
};

export async function translateText(text, targetLanguage) {
  // Don't translate if target is English
  if (targetLanguage === 'en-US' || !targetLanguage) {
    return text;
  }

  // Check cache first
  const cacheKey = `${text.substring(0, 50)}_${targetLanguage}`;
  if (TRANSLATION_CACHE.has(cacheKey)) {
    return TRANSLATION_CACHE.get(cacheKey);
  }

  try {
    const targetLang = LANGUAGE_MAP[targetLanguage] || 'en';
    
    // Use MyMemory Translation API (free)
    const response = await fetch(
      `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=en|${targetLang}`
    );
    
    const data = await response.json();
    
    if (data.responseStatus === 200 && data.responseData) {
      const translated = data.responseData.translatedText;
      TRANSLATION_CACHE.set(cacheKey, translated);
      return translated;
    }
    
    // Fallback to original text if translation fails
    return text;
  } catch (error) {
    console.error('Translation error:', error);
    return text; // Return original text on error
  }
}

export async function translateLesson(lesson, targetLanguage) {
  if (targetLanguage === 'en-US' || !targetLanguage) {
    return lesson;
  }

  try {
    // Translate key fields
    const [translatedTitle, translatedDescription, translatedContent] = await Promise.all([
      translateText(lesson.title.en, targetLanguage),
      translateText(lesson.description.en, targetLanguage),
      translateText(lesson.content.en, targetLanguage)
    ]);

    return {
      ...lesson,
      title: {
        ...lesson.title,
        translated: translatedTitle
      },
      description: {
        ...lesson.description,
        translated: translatedDescription
      },
      content: {
        ...lesson.content,
        translated: translatedContent
      }
    };
  } catch (error) {
    console.error('Lesson translation error:', error);
    return lesson;
  }
}
