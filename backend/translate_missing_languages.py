"""
Translate missing languages: Hindi, Bengali, Marathi, Telugu, Thai, Filipino, Malay
And complete: Mandarin, Cantonese
"""

import asyncio
import os
import time
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from google.cloud import translate_v2 as translate
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, '.env'))

# Set Google credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(SCRIPT_DIR, 'google_cloud_key.json')

# Languages to translate
LANGUAGES = {
    'hi': 'Hindi',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Filipino',
    'ms': 'Malay',
    'zh': 'Mandarin',
    'yue': 'Cantonese'
}

GOOGLE_LANG_CODES = {
    'hi': 'hi',
    'bn': 'bn',
    'mr': 'mr',
    'te': 'te',
    'th': 'th',
    'tl': 'tl',
    'ms': 'ms',
    'zh': 'zh-CN',
    'yue': 'zh-TW'
}

class GoogleTranslator:
    def __init__(self):
        self.client = translate.Client()
        print("✅ Google Cloud Translation API initialized")
    
    def translate_text(self, text, target_lang):
        """Translate text using Google Cloud"""
        if not text or len(text.strip()) == 0:
            return text
            
        try:
            google_code = GOOGLE_LANG_CODES.get(target_lang, target_lang)
            result = self.client.translate(
                text,
                target_language=google_code,
                source_language='en'
            )
            return result['translatedText']
        except Exception as e:
            print(f"    ⚠️  Translation error for {target_lang}: {e}")
            return text
    
    async def translate_lesson(self, lesson, lessons_collection, idx, total):
        """Translate one lesson to missing languages"""
        title_en = lesson['title'].get('en', '')
        desc_en = lesson['description'].get('en', '')
        content_en = lesson['content'].get('en', '')[:2000]
        
        title_preview = title_en[:50]
        print(f"  📖 [{idx}/{total}] {title_preview}...")
        
        updates = {}
        success_count = 0
        
        for lang_code, lang_name in LANGUAGES.items():
            # Skip if already translated
            if lesson['title'].get(lang_code):
                continue
                
            try:
                # Translate all fields
                title_translated = self.translate_text(title_en, lang_code)
                desc_translated = self.translate_text(desc_en, lang_code)
                content_translated = self.translate_text(content_en, lang_code)
                
                updates[f'title.{lang_code}'] = title_translated
                updates[f'description.{lang_code}'] = desc_translated
                updates[f'content.{lang_code}'] = content_translated
                
                success_count += 1
                print(f"    ✅ {lang_name}: {title_translated[:30]}...")
            except Exception as e:
                print(f"    ❌ {lang_name}: {e}")
        
        # Update database
        if updates:
            await lessons_collection.update_one(
                {'id': lesson['id']},
                {'$set': updates}
            )
        
        return success_count

async def translate_all():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    lessons_collection = db.lessons
    
    print("\n🚀 Starting translation for missing languages...\n")
    
    # Get all lessons
    all_lessons = await lessons_collection.find({}).to_list(length=1100)
    
    # Filter lessons that need translation
    to_translate = []
    for lesson in all_lessons:
        needs_translation = False
        for lang_code in LANGUAGES.keys():
            if not lesson['title'].get(lang_code):
                needs_translation = True
                break
        if needs_translation:
            to_translate.append(lesson)
    
    total = len(to_translate)
    print(f"📚 Total lessons: {len(all_lessons)}")
    print(f"📝 Need translation: {total}")
    print(f"🌍 Languages: {', '.join(LANGUAGES.values())}\n")
    
    if total == 0:
        print("🎉 All lessons already translated!")
        client.close()
        return
    
    translator = GoogleTranslator()
    start_time = time.time()
    total_translations = 0
    
    # Process lessons
    for idx, lesson in enumerate(to_translate, 1):
        success = await translator.translate_lesson(lesson, lessons_collection, idx, total)
        total_translations += success
        
        # Progress report every 50 lessons
        if idx % 50 == 0 or idx == total:
            elapsed = time.time() - start_time
            rate = idx / elapsed if elapsed > 0 else 0
            eta_mins = ((total - idx) / rate / 60) if rate > 0 else 0
            pct = (idx / total) * 100
            
            print(f"\n  {'='*50}")
            print(f"  📊 PROGRESS: {idx}/{total} ({pct:.1f}%)")
            print(f"  ✅ Translations: {total_translations}")
            print(f"  ⏱️  Elapsed: {elapsed/60:.1f}min | ETA: {eta_mins:.1f}min")
            print(f"  🚀 Speed: {rate:.2f} lessons/sec")
            print(f"  {'='*50}\n")
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"🎉 TRANSLATION COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ Lessons: {total}")
    print(f"✅ Translations: {total_translations}")
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"🌍 Languages: {', '.join(LANGUAGES.values())}")
    print(f"{'='*70}\n")
    
    client.close()

if __name__ == "__main__":
    print("\n🚀 Starting Google Cloud Translation for Missing Languages...\n")
    asyncio.run(translate_all())
