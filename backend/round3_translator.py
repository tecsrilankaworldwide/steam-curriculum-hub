"""
Round 3 Translation: 7 More Languages
Hindi, Bengali, Marathi, Telugu, Thai, Filipino, Malay
Using Google Cloud Translation API
"""

import asyncio
import os
import time
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from google.cloud import translate_v2 as translate

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, '.env'))

# Set Google credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(SCRIPT_DIR, 'google_cloud_key.json')

# Round 3: 7 new languages
LANGUAGES = {
    'hi': 'Hindi',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Filipino',
    'ms': 'Malay'
}

class Round3Translator:
    def __init__(self):
        try:
            self.client = translate.Client()
            print("✅ Google Cloud Translation API initialized")
            print(f"⚡ Round 3: {len(LANGUAGES)} languages")
        except Exception as e:
            print(f"❌ Failed to initialize Google Cloud: {e}")
            self.client = None
    
    def translate_text(self, text, target_lang):
        """Translate text using Google Cloud Translation API"""
        if not text or len(text.strip()) == 0 or not self.client:
            return text
            
        try:
            result = self.client.translate(
                text,
                target_language=target_lang,
                source_language='en'
            )
            return result['translatedText']
        except Exception as e:
            print(f"    ⚠️  Translation error for {target_lang}: {str(e)[:100]}")
            return text
    
    async def translate_lesson(self, lesson, lessons_collection, idx, total):
        """Translate one lesson to all Round 3 languages"""
        title_en = lesson['title'].get('en', '')
        desc_en = lesson['description'].get('en', '')
        content_en = lesson['content'].get('en', '')[:2000]
        
        title_preview = title_en[:50]
        print(f"  📖 [{idx}/{total}] {title_preview}...")
        
        # Get existing translations
        title_update = {**lesson['title']}
        desc_update = {**lesson['description']}
        content_update = {**lesson['content']}
        
        success_count = 0
        
        for lang_code, lang_name in LANGUAGES.items():
            # Skip if already translated
            if lang_code in title_update and title_update[lang_code]:
                success_count += 1
                continue
                
            try:
                # Translate all fields
                title_translated = self.translate_text(title_en, lang_code)
                desc_translated = self.translate_text(desc_en, lang_code)
                content_translated = self.translate_text(content_en, lang_code)
                
                title_update[lang_code] = title_translated
                desc_update[lang_code] = desc_translated
                content_update[lang_code] = content_translated
                
                success_count += 1
            except Exception as e:
                print(f"    ❌ Error translating to {lang_name}: {e}")
        
        # Update database
        if success_count > 0:
            try:
                # Get existing translated languages
                existing_langs = lesson.get('languages_translated', [])
                new_langs = list(set(existing_langs + list(LANGUAGES.keys())))
                
                await lessons_collection.update_one(
                    {"id": lesson["id"]},
                    {"$set": {
                        "title": title_update,
                        "description": desc_update,
                        "content": content_update,
                        "languages_translated": new_langs,
                        "round3_complete": True
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
    
    translator = Round3Translator()
    
    if not translator.client:
        print("❌ Cannot proceed without Google Cloud Translation API")
        client.close()
        return
    
    print("\n" + "="*70)
    print("     🌍 ROUND 3: 7 MORE LANGUAGES")
    print("="*70)
    
    # Get all AI lessons
    ai_lessons = await lessons_collection.find(
        {"is_ai_curriculum": True}
    ).to_list(length=1100)
    
    print(f"\n📚 Total AI lessons: {len(ai_lessons)}")
    print(f"🌍 Languages: {', '.join(LANGUAGES.values())}")
    print(f"⚡ Using Google Cloud Translation API")
    
    print(f"\n🚀 Starting Round 3 translation...\n")
    
    total_translations = 0
    start_time = time.time()
    total = len(ai_lessons)
    
    # Process all lessons
    for idx, lesson in enumerate(ai_lessons, 1):
        success = await translator.translate_lesson(lesson, lessons_collection, idx, total)
        total_translations += success
        
        # Progress report every 100 lessons
        if idx % 100 == 0 or idx == total:
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
    print(f"🎉 ROUND 3 TRANSLATION COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ Lessons: {total}")
    print(f"✅ Translations: {total_translations}")
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"🌍 Languages: {', '.join(LANGUAGES.values())}")
    print(f"{'='*70}\n")
    
    client.close()


if __name__ == "__main__":
    print("\n🚀 Starting Round 3 Translation (7 Languages)...\n")
    asyncio.run(translate_all())
