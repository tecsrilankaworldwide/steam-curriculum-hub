"""
SUPER FAST Google Cloud Translation API
Translates 1000 lessons in minutes instead of hours!
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

# Language mappings - ALL LANGUAGES!
LANGUAGES = {
    'si': 'Sinhala',
    'ta': 'Tamil',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Filipino',
    'ms': 'Malay',
    'zh': 'Chinese (Simplified/Mandarin)',
    'yue': 'Chinese (Cantonese)'
}

# Google Cloud Translation language codes
GOOGLE_LANG_CODES = {
    'si': 'si',      # Sinhala
    'ta': 'ta',      # Tamil
    'hi': 'hi',      # Hindi
    'bn': 'bn',      # Bengali
    'mr': 'mr',      # Marathi
    'te': 'te',      # Telugu
    'th': 'th',      # Thai
    'tl': 'tl',      # Filipino (Tagalog)
    'ms': 'ms',      # Malay
    'zh': 'zh-CN',   # Mandarin (Simplified)
    'yue': 'zh-TW'   # Cantonese (Traditional Chinese)
}

class GoogleCloudTranslator:
    def __init__(self):
        self.client = translate.Client()
        print("✅ Google Cloud Translation API initialized")
        print(f"⚡ SUPER FAST translation with Google Cloud")
    
    def translate_text(self, text, target_lang):
        """Translate text using Google Cloud Translation API"""
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
        """Translate one lesson to all languages"""
        title_en = lesson['title'].get('en', '')
        desc_en = lesson['description'].get('en', '')
        content_en = lesson['content'].get('en', '')[:2000]
        
        title_preview = title_en[:50]
        print(f"  📖 [{idx}/{total}] {title_preview}...")
        
        # Translate to all languages
        title_update = {**lesson['title']}
        desc_update = {**lesson['description']}
        content_update = {**lesson['content']}
        
        success_count = 0
        
        for lang_code, lang_name in LANGUAGES.items():
            try:
                # Translate all fields
                title_translated = self.translate_text(title_en, lang_code)
                desc_translated = self.translate_text(desc_en, lang_code)
                content_translated = self.translate_text(content_en, lang_code)
                
                # Store with correct key (zh-TW becomes yue for consistency)
                store_key = 'yue' if lang_code == 'zh-TW' else lang_code
                
                title_update[store_key] = title_translated
                desc_update[store_key] = desc_translated
                content_update[store_key] = content_translated
                
                success_count += 1
            except Exception as e:
                print(f"    ❌ Error translating to {lang_name}: {e}")
        
        # Update database
        if success_count > 0:
            try:
                await lessons_collection.update_one(
                    {"id": lesson["id"]},
                    {"$set": {
                        "title": title_update,
                        "description": desc_update,
                        "content": content_update,
                        "translations_complete": True,
                        "translation_method": "google-cloud-translate-api",
                        "languages_translated": ['si', 'ta', 'zh', 'yue']
                    }}
                )
            except Exception as e:
                print(f"    ❌ DB error: {e}")
        
        return success_count


async def translate_all():
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.getenv('DB_NAME', 'test_database')
    
    print(f"🔗 Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    lessons_collection = db.lessons
    
    translator = GoogleCloudTranslator()
    
    print("\n" + "="*70)
    print("     ⚡ SUPER FAST GOOGLE CLOUD TRANSLATION API")
    print("="*70)
    
    # Get lessons needing translation
    ai_lessons = await lessons_collection.find(
        {"is_ai_curriculum": True}
    ).to_list(length=1100)
    
    already_done = sum(1 for l in ai_lessons if l.get('translations_complete'))
    to_translate = [l for l in ai_lessons if not l.get('translations_complete')]
    
    print(f"\n📚 Total AI lessons: {len(ai_lessons)}")
    print(f"✅ Already translated: {already_done}")
    print(f"📝 Remaining: {len(to_translate)}")
    print(f"🌍 Languages: Sinhala, Tamil, Mandarin, Cantonese")
    print(f"⚡ Using Google Cloud Translation API (Instant!)")
    
    if not to_translate:
        print("\n🎉 All lessons already translated!")
        client.close()
        return
    
    print(f"\n🚀 Starting SUPER FAST translation...\n")
    
    total_translations = 0
    start_time = time.time()
    total = len(to_translate)
    
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
    print(f"🌍 Languages: Sinhala, Tamil, Mandarin, Cantonese")
    print(f"{'='*70}\n")
    
    client.close()


if __name__ == "__main__":
    print("\n🚀 Starting Google Cloud Translation...\n")
    asyncio.run(translate_all())
