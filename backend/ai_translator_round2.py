"""
AI-Powered Translation System - ROUND 2
Mandarin (Chinese Simplified) + Cantonese (Chinese Traditional/HK)
Uses GPT-4o-mini via Emergent LLM Key (faster + cheaper)
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

# Round 2: Mandarin + Cantonese
TARGET_LANGUAGES = {
    "zh": "Chinese Simplified (Mandarin)",
    "yue": "Chinese Traditional (Cantonese)",
}

# Concurrency settings for GPT-4o-mini (faster model, can handle more)
SEMAPHORE_LIMIT = 2
API_TIMEOUT = 90

class Round2Translator:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
        self.semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
        print(f"✅ Round 2 Translator initialized with GPT-4o-mini")
        print(f"⚡ Languages: {', '.join(TARGET_LANGUAGES.values())}")
        print(f"⚡ Max concurrent: {SEMAPHORE_LIMIT}")
    
    def _make_chat(self, session_tag):
        """Create a fresh LlmChat instance using GPT-4o-mini"""
        return LlmChat(
            api_key=self.api_key,
            session_id=f"r2-trans-{session_tag}-{int(time.time())}",
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
        ).with_model("openai", "gpt-4o-mini")
    
    async def translate_lesson_to_lang(self, lesson, lang_code, lang_name):
        """Translate all parts of a lesson in ONE API call"""
        async with self.semaphore:
            title_en = lesson['title'].get('en', '')
            desc_en = lesson['description'].get('en', '')
            content_en = lesson['content'].get('en', '')[:2000]
            
            # Special instructions for Cantonese
            extra = ""
            if lang_code == "yue":
                extra = "\nIMPORTANT: Use Traditional Chinese characters (繁體中文) as used in Hong Kong. Use Cantonese vocabulary and phrasing where different from Mandarin."
            
            combined = f"""Translate the following children's AI education content to {lang_name}.{extra}

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
        """Translate one lesson to both Chinese languages in parallel"""
        title_preview = lesson['title'].get('en', 'Unknown')[:45]
        print(f"  📖 [{lesson_idx}/{total}] {title_preview}...")
        
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
            # Get existing languages_translated list
            existing_langs = lesson.get('languages_translated', [])
            new_langs = list(set(existing_langs + [lc for lc in TARGET_LANGUAGES.keys()]))
            
            try:
                await lessons_collection.update_one(
                    {"id": lesson["id"]},
                    {"$set": {
                        "title": title_update,
                        "description": desc_update,
                        "content": content_update,
                        "languages_translated": new_langs,
                        "round2_complete": True,
                    }}
                )
            except Exception as e:
                print(f"    ❌ DB error: {e}")
                error_count += 1
        
        return success_count, error_count


async def translate_all():
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.getenv('DB_NAME', 'steam_hub')
    
    print(f"🔗 Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    lessons_collection = db.lessons
    
    translator = Round2Translator()
    
    print("\n" + "="*70)
    print("     🇨🇳 ROUND 2: MANDARIN + CANTONESE (GPT-4o-mini)")
    print("="*70)
    
    # Get all AI lessons that DON'T have round2 translations yet
    ai_lessons = await lessons_collection.find(
        {"is_ai_curriculum": True, "round2_complete": {"$ne": True}}
    ).to_list(length=1100)
    
    already_done = await lessons_collection.count_documents(
        {"is_ai_curriculum": True, "round2_complete": True}
    )
    
    print(f"\n📚 To translate: {len(ai_lessons)}")
    print(f"✅ Already done: {already_done}")
    print(f"🌍 Languages: {', '.join(TARGET_LANGUAGES.values())}")
    print(f"📊 API calls needed: ~{len(ai_lessons) * 2}")
    
    if not ai_lessons:
        print("\n🎉 All lessons already translated! Nothing to do.")
        client.close()
        return
    
    print(f"\n🚀 Starting Round 2 translation...\n")
    
    total_translations = 0
    total_errors = 0
    start_time = time.time()
    total = len(ai_lessons)
    
    for idx, lesson in enumerate(ai_lessons, 1):
        success, errors = await translator.translate_one_lesson(lesson, lessons_collection, idx, total)
        total_translations += success
        total_errors += errors
        
        if idx % 25 == 0 or idx == total:
            elapsed = time.time() - start_time
            rate = idx / elapsed if elapsed > 0 else 0
            eta_mins = ((total - idx) / rate / 60) if rate > 0 else 0
            pct = (idx / total) * 100
            
            print(f"\n  {'='*50}")
            print(f"  📊 PROGRESS: {idx}/{total} ({pct:.1f}%)")
            print(f"  ✅ Translations: {total_translations} | ❌ Errors: {total_errors}")
            print(f"  ⏱️ Elapsed: {elapsed/60:.1f}min | ETA: {eta_mins:.1f}min")
            print(f"  {'='*50}\n")
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"🎉 ROUND 2 TRANSLATION COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ Lessons: {total}")
    print(f"✅ Translations: {total_translations}")
    print(f"❌ Errors: {total_errors}")
    print(f"⏱️ Time: {elapsed/60:.1f} minutes")
    print(f"{'='*70}\n")
    
    client.close()

if __name__ == "__main__":
    print("\n🚀 Starting Round 2 Translation (Mandarin + Cantonese)...\n")
    asyncio.run(translate_all())
