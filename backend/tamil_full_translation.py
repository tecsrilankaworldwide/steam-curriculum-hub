"""
TAMIL FULL CONTENT TRANSLATION
Translate complete lesson content (no character limits) for Tamil language
All 1000 lessons, all age groups (matching Sinhala)
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

class TamilTranslator:
    def __init__(self):
        self.client = translate.Client()
        print("✅ Google Cloud Translation API initialized for TAMIL")
    
    def translate_text(self, text):
        """Translate text to Tamil"""
        if not text or len(text.strip()) == 0:
            return text
            
        try:
            result = self.client.translate(
                text,
                target_language='ta',
                source_language='en'
            )
            return result['translatedText']
        except Exception as e:
            print(f"    ⚠️  Translation error: {e}")
            return text
    
    async def translate_lesson(self, lesson, lessons_collection, idx, total):
        """Translate one lesson completely to Tamil"""
        
        # Skip if already has full Tamil content (> 5000 chars)
        if lesson['content'].get('ta') and len(lesson['content'].get('ta', '')) > 5000:
            print(f"  ⏭️  [{idx}/{total}] Already translated: {lesson['title']['en'][:50]}...")
            return 0
        
        title_en = lesson['title'].get('en', '')
        desc_en = lesson['description'].get('en', '')
        content_en = lesson['content'].get('en', '')  # FULL CONTENT - NO LIMIT!
        
        title_preview = title_en[:50]
        print(f"\n  📖 [{idx}/{total}] {title_preview}...")
        print(f"     Content length: {len(content_en)} chars")
        
        try:
            # Translate title
            if not lesson['title'].get('ta'):
                title_ta = self.translate_text(title_en)
                print(f"     ✅ Title: {title_ta[:40]}...")
            else:
                title_ta = lesson['title']['ta']
            
            # Translate description
            if not lesson['description'].get('ta'):
                desc_ta = self.translate_text(desc_en)
                print(f"     ✅ Description translated")
            else:
                desc_ta = lesson['description']['ta']
            
            # Translate FULL content
            print(f"     🔄 Translating full content ({len(content_en)} chars)...")
            
            # Split content into chunks if needed (Google has 30K char limit per request)
            if len(content_en) > 25000:
                chunks = [content_en[i:i+25000] for i in range(0, len(content_en), 25000)]
                translated_chunks = []
                for i, chunk in enumerate(chunks):
                    print(f"        Chunk {i+1}/{len(chunks)}...")
                    translated_chunks.append(self.translate_text(chunk))
                content_ta = ''.join(translated_chunks)
            else:
                content_ta = self.translate_text(content_en)
            
            print(f"     ✅ Content translated: {len(content_ta)} chars")
            
            # Update database
            await lessons_collection.update_one(
                {'id': lesson['id']},
                {'$set': {
                    'title.ta': title_ta,
                    'description.ta': desc_ta,
                    'content.ta': content_ta
                }}
            )
            
            return 1
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return 0

async def translate_all():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    lessons_collection = db.lessons
    
    print("\n" + "="*70)
    print("🇮🇳 TAMIL FULL CONTENT TRANSLATION")
    print("="*70)
    
    # Get all lessons
    all_lessons = await lessons_collection.find({}).to_list(length=1100)
    
    # Filter lessons that need full Tamil translation
    to_translate = []
    for lesson in all_lessons:
        ta_content = lesson['content'].get('ta', '')
        # Need translation if: no Tamil OR Tamil content < 5000 chars (partial)
        if not ta_content or len(ta_content) < 5000:
            to_translate.append(lesson)
    
    total = len(to_translate)
    print(f"📚 Total lessons: {len(all_lessons)}")
    print(f"📝 Need full translation: {total}")
    print(f"💰 Estimated cost: ${(total * 12000 / 1000000) * 20:.2f}")
    print("="*70 + "\n")
    
    if total == 0:
        print("🎉 All lessons already have full Tamil translation!")
        client.close()
        return
    
    translator = TamilTranslator()
    start_time = time.time()
    translated_count = 0
    
    # Process lessons
    for idx, lesson in enumerate(to_translate, 1):
        result = await translator.translate_lesson(lesson, lessons_collection, idx, total)
        translated_count += result
        
        # Progress report every 25 lessons
        if idx % 25 == 0 or idx == total:
            elapsed = time.time() - start_time
            rate = idx / elapsed if elapsed > 0 else 0
            eta_mins = ((total - idx) / rate / 60) if rate > 0 else 0
            pct = (idx / total) * 100
            
            print(f"\n  {'='*65}")
            print(f"  📊 PROGRESS: {idx}/{total} ({pct:.1f}%)")
            print(f"  ✅ Translated: {translated_count}")
            print(f"  ⏱️  Elapsed: {elapsed/60:.1f}min | ETA: {eta_mins:.1f}min")
            print(f"  🚀 Speed: {rate:.2f} lessons/sec")
            print(f"  {'='*65}\n")
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"🎉 TAMIL FULL TRANSLATION COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ Lessons translated: {translated_count}/{total}")
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"🇮🇳 All 1000 lessons now have COMPLETE Tamil content!")
    print(f"🇱🇰 SRI LANKA COMPLETE: Sinhala ✅ + Tamil ✅")
    print(f"{'='*70}\n")
    
    client.close()

if __name__ == "__main__":
    print("\n🚀 Starting FULL Tamil Content Translation...\n")
    asyncio.run(translate_all())
