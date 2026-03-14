"""
SUPER FAST Translation with Google Gemini
Translates all 4 languages in parallel (Sinhala, Tamil, Mandarin, Cantonese)
Uses Gemini 2.0 Flash - MUCH faster than GPT
"""

import asyncio
import os
import time
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, '.env'))

# ALL 4 LANGUAGES AT ONCE
TARGET_LANGUAGES = {
    "si": "Sinhala",
    "ta": "Tamil",
    "zh": "Chinese Simplified (Mandarin)",
    "yue": "Chinese Traditional (Cantonese)",
}

# Gemini is FAST - can handle more concurrent requests
CONCURRENT_LESSONS = 5  # Process 5 lessons at once
SEMAPHORE_LIMIT = 10    # 10 API calls in parallel
API_TIMEOUT = 60

class GeminiFastTranslator:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found")
        self.semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
        print(f"✅ Gemini Fast Translator initialized")
        print(f"⚡ Using Google Gemini 2.0 Flash (SUPER FAST)")
        print(f"⚡ Max concurrent API calls: {SEMAPHORE_LIMIT}")
        print(f"⚡ Processing {CONCURRENT_LESSONS} lessons at once")
    
    def _make_chat(self, session_tag):
        """Create Gemini chat instance"""
        return LlmChat(
            api_key=self.api_key,
            session_id=f"gemini-trans-{session_tag}-{int(time.time())}",
            system_message="""You are an expert educational content translator for children's AI education.
Translate accurately while maintaining technical precision and age-appropriate language.

Input format:
[TITLE] ... [/TITLE]
[DESC] ... [/DESC]
[CONTENT] ... [/CONTENT]

Return EXACT same format with translated text. Keep tags in English."""
        ).with_model("google", "gemini-2.0-flash-exp")
    
    async def translate_lesson_to_lang(self, lesson, lang_code, lang_name):
        """Translate one lesson to one language"""
        async with self.semaphore:
            title_en = lesson['title'].get('en', '')
            desc_en = lesson['description'].get('en', '')
            content_en = lesson['content'].get('en', '')[:2000]
            
            extra = ""
            if lang_code == "yue":
                extra = "\nUse Traditional Chinese (繁體中文) with Cantonese vocabulary."
            
            combined = f"""Translate to {lang_name}.{extra}

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
        start_tag = f"[{tag}]"
        end_tag = f"[/{tag}]"
        start = text.find(start_tag)
        end = text.find(end_tag)
        if start != -1 and end != -1:
            return text[start + len(start_tag):end].strip()
        return None
    
    async def translate_one_lesson(self, lesson, lessons_collection, lesson_idx, total):
        """Translate one lesson to ALL 4 languages in parallel"""
        title_preview = lesson['title'].get('en', 'Unknown')[:45]
        print(f"  📖 [{lesson_idx}/{total}] {title_preview}...")
        
        # Launch all 4 languages at once
        tasks = [
            self.translate_lesson_to_lang(lesson, lc, ln)
            for lc, ln in TARGET_LANGUAGES.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
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
        
        if success_count > 0:
            try:
                await lessons_collection.update_one(
                    {"id": lesson["id"]},
                    {"$set": {
                        "title": title_update,
                        "description": desc_update,
                        "content": content_update,
                        "translations_complete": True,
                        "translation_method": "gemini-2.0-flash",
                        "languages_translated": list(TARGET_LANGUAGES.keys())
                    }}
                )
            except Exception as e:
                print(f"    ❌ DB error: {e}")
                error_count += 1
        
        return success_count, error_count


async def translate_all():
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.getenv('DB_NAME', 'test_database')
    
    print(f"🔗 Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    lessons_collection = db.lessons
    
    translator = GeminiFastTranslator()
    
    print("\n" + "="*70)
    print("     🚀 SUPER FAST TRANSLATION WITH GOOGLE GEMINI 2.0")
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
    print(f"⚡ Processing: {CONCURRENT_LESSONS} lessons × 4 languages in parallel")
    print(f"📊 API calls needed: ~{len(to_translate) * 4}")
    
    if not to_translate:
        print("\n🎉 All lessons already translated!")
        client.close()
        return
    
    print(f"\n🚀 Starting SUPER FAST translation...\n")
    
    total_translations = 0
    total_errors = 0
    start_time = time.time()
    total = len(to_translate)
    
    # Process in batches
    for batch_start in range(0, total, CONCURRENT_LESSONS):
        batch = to_translate[batch_start:batch_start + CONCURRENT_LESSONS]
        
        tasks = [
            translator.translate_one_lesson(lesson, lessons_collection, batch_start + i + 1, total)
            for i, lesson in enumerate(batch)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for r in results:
            if isinstance(r, Exception):
                total_errors += 1
            else:
                total_translations += r[0]
                total_errors += r[1]
        
        done = min(batch_start + CONCURRENT_LESSONS, total)
        if done % 50 < CONCURRENT_LESSONS or done == total:
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
    print(f"✅ Lessons: {total}")
    print(f"✅ Translations: {total_translations}")
    print(f"❌ Errors: {total_errors}")
    print(f"⏱️ Time: {elapsed/60:.1f} minutes ({elapsed/3600:.1f} hours)")
    print(f"🌍 Languages: {', '.join(TARGET_LANGUAGES.values())}")
    print(f"{'='*70}\n")
    
    client.close()

if __name__ == "__main__":
    print("\n🚀 Starting SUPER FAST Gemini Translation...\n")
    asyncio.run(translate_all())
