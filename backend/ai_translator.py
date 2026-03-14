"""
AI-Powered Translation System for 1000+ Lessons (V3 - FAST)
Uses OpenAI GPT-5.2 via Emergent LLM Key
OPTIMIZED: Single API call per language + concurrent lessons
"""

import asyncio
import json
import os
import time
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Get script directory and load .env
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, '.env'))

# ROUND 1: Sinhala + Tamil (GPT-5.2 - high quality)
TARGET_LANGUAGES = {
    "si": "Sinhala",
    "ta": "Tamil",
}

# Process 1 lesson at a time (2 languages in parallel per lesson)
CONCURRENT_LESSONS = 1
# Timeout per API call in seconds
API_TIMEOUT = 120

class FastTranslator:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
        # Allow both languages to translate concurrently
        self.semaphore = asyncio.Semaphore(2)
        print(f"✅ Fast Translator initialized with GPT-5.2")
        print(f"⚡ Max concurrent API calls: 2 (Sinhala + Tamil in parallel)")
    
    def _make_chat(self, session_tag):
        """Create a fresh LlmChat instance"""
        return LlmChat(
            api_key=self.api_key,
            session_id=f"fast-trans-{session_tag}-{int(time.time())}",
            system_message="""You are an expert educational content translator for children's AI education.
Translate accurately while maintaining:
- Technical terminology precision
- Age-appropriate language and tone
- Educational quality
- Original formatting (newlines, bullets, headers)

You will receive content in this format:
[TITLE] ... [/TITLE]
[DESC] ... [/DESC]
[CONTENT] ... [/CONTENT]

Return the translation in the EXACT same format with the translated text. Only translate the text between tags, keep the tags in English."""
        ).with_model("openai", "gpt-5.2")
    
    async def translate_lesson_to_lang(self, lesson, lang_code, lang_name):
        """Translate all parts of a lesson in ONE API call (with semaphore)"""
        async with self.semaphore:
            title_en = lesson['title'].get('en', '')
            desc_en = lesson['description'].get('en', '')
            content_en = lesson['content'].get('en', '')[:2000]
            
            # Combine all fields into one prompt
            combined = f"""Translate the following children's AI education content to {lang_name}:

[TITLE]{title_en}[/TITLE]
[DESC]{desc_en}[/DESC]
[CONTENT]{content_en}[/CONTENT]"""
            
            try:
                chat = self._make_chat(f"{lang_code}-{lesson['id'][:8]}")
                response = await asyncio.wait_for(
                    chat.send_message(UserMessage(text=combined)),
                    timeout=API_TIMEOUT
                )
                resp = response.strip()
                
                # Parse response
                title_t = self._extract_tag(resp, 'TITLE') or title_en
                desc_t = self._extract_tag(resp, 'DESC') or desc_en
                content_t = self._extract_tag(resp, 'CONTENT') or content_en
                
                return {
                    "lang_code": lang_code,
                    "title": title_t,
                    "description": desc_t,
                    "content": content_t,
                    "success": True
                }
            except Exception as e:
                return {
                    "lang_code": lang_code,
                    "title": f"[{lang_name} pending]",
                    "description": f"[{lang_name} pending]",
                    "content": f"[{lang_name} pending]",
                    "success": False,
                    "error": str(e)
                }
    
    def _extract_tag(self, text, tag):
        """Extract content between [TAG] and [/TAG]"""
        start_tag = f"[{tag}]"
        end_tag = f"[/{tag}]"
        
        start = text.find(start_tag)
        end = text.find(end_tag)
        
        if start != -1 and end != -1:
            return text[start + len(start_tag):end].strip()
        return None
    
    async def translate_one_lesson(self, lesson, lessons_collection, lesson_idx, total):
        """Translate one lesson to all 9 languages in parallel"""
        title_preview = lesson['title'].get('en', 'Unknown')[:45]
        print(f"  📖 [{lesson_idx}/{total}] {title_preview}...")
        
        # Launch all 9 language translations in parallel
        tasks = [
            self.translate_lesson_to_lang(lesson, lc, ln) 
            for lc, ln in TARGET_LANGUAGES.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        title_update = {**lesson['title']}
        desc_update = {**lesson['description']}
        content_update = {**lesson['content']}
        success_count = 0
        error_count = 0
        
        for r in results:
            if isinstance(r, Exception):
                error_count += 1
                continue
            if r.get('success'):
                lc = r['lang_code']
                title_update[lc] = r['title']
                desc_update[lc] = r['description']
                content_update[lc] = r['content']
                success_count += 1
            else:
                error_count += 1
        
        # Save to database
        if success_count > 0:
            try:
                await lessons_collection.update_one(
                    {"id": lesson["id"]},
                    {"$set": {
                        "title": title_update,
                        "description": desc_update,
                        "content": content_update,
                        "translations_complete": True,
                        "translation_method": "ai_gpt5.2_fast",
                        "languages_translated": [lc for lc in TARGET_LANGUAGES.keys()]
                    }}
                )
            except Exception as e:
                print(f"    ❌ DB error: {e}")
                error_count += 1
        
        return success_count, error_count


async def translate_all_lessons():
    """Main translation function - processes lessons in concurrent batches"""
    
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.getenv('DB_NAME', 'steam_hub')
    
    print(f"🔗 Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    lessons_collection = db.lessons
    
    translator = FastTranslator()
    
    print("\n" + "="*70)
    print("     🌍 FAST TRANSLATION (1 API call/language + concurrent lessons)")
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
    print(f"🌍 Languages: {len(TARGET_LANGUAGES)} ({', '.join(TARGET_LANGUAGES.values())})")
    print(f"⚡ Speed: {CONCURRENT_LESSONS} lessons × 9 languages in parallel")
    print(f"📊 API calls needed: ~{len(to_translate) * 9} (1 per language per lesson)")
    
    if not to_translate:
        print("\n🎉 All lessons already translated! Nothing to do.")
        client.close()
        return
    
    print(f"\n🚀 Starting translation...\n")
    
    total_translations = 0
    total_errors = 0
    start_time = time.time()
    total = len(to_translate)
    
    # Process in batches of CONCURRENT_LESSONS
    for batch_start in range(0, total, CONCURRENT_LESSONS):
        batch = to_translate[batch_start:batch_start + CONCURRENT_LESSONS]
        batch_num = (batch_start // CONCURRENT_LESSONS) + 1
        
        # Run batch concurrently
        tasks = [
            translator.translate_one_lesson(lesson, lessons_collection, batch_start + i + 1, total)
            for i, lesson in enumerate(batch)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for r in results:
            if isinstance(r, Exception):
                total_errors += 1
                print(f"    ❌ Batch error: {r}")
            else:
                total_translations += r[0]
                total_errors += r[1]
        
        # Progress report every 25 lessons
        done = min(batch_start + CONCURRENT_LESSONS, total)
        if done % 25 < CONCURRENT_LESSONS or done == total:
            elapsed = time.time() - start_time
            rate = done / elapsed if elapsed > 0 else 0
            eta_mins = ((total - done) / rate / 60) if rate > 0 else 0
            pct = (done / total) * 100
            
            print(f"\n  {'='*50}")
            print(f"  📊 PROGRESS: {done}/{total} ({pct:.1f}%)")
            print(f"  ✅ Translations: {total_translations} | ❌ Errors: {total_errors}")
            print(f"  ⏱️ Elapsed: {elapsed/60:.1f}min | ETA: {eta_mins:.1f}min")
            print(f"  🚀 Speed: {rate:.2f} lessons/sec")
            print(f"  {'='*50}\n")
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"🎉 TRANSLATION COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ Lessons translated: {total}")
    print(f"✅ Total translations: {total_translations}")
    print(f"❌ Errors: {total_errors}")
    print(f"⏱️ Total time: {elapsed/60:.1f} minutes")
    print(f"🌍 Languages: {', '.join(TARGET_LANGUAGES.values())}")
    print(f"{'='*70}\n")
    
    client.close()

if __name__ == "__main__":
    print("\n🚀 Starting FAST Translation System...\n")
    asyncio.run(translate_all_lessons())
