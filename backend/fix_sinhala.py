"""
Fix Missing Sinhala Translations
Some lessons only have Hindi but not Sinhala - fix them now!
"""

import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from google.cloud import translate_v2 as translate

load_dotenv('/app/backend/.env')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/app/backend/google_cloud_key.json'

async def fix_missing_sinhala():
    mongo_url = os.getenv('MONGO_URL')
    db_name = os.getenv('DB_NAME')
    
    client_motor = AsyncIOMotorClient(mongo_url)
    db = client_motor[db_name]
    lessons_collection = db.lessons
    
    translator = translate.Client()
    
    # Find lessons WITHOUT proper Sinhala but WITH English
    lessons_need_fix = await lessons_collection.find({
        'is_ai_curriculum': True,
        '$or': [
            {'title.si': {'$exists': False}},
            {'title.si': None},
            {'title.si': ''},
            {'$expr': {'$eq': ['$title.si', '$title.en']}}  # Sinhala same as English
        ]
    }).to_list(length=500)
    
    print(f"Found {len(lessons_need_fix)} lessons needing Sinhala translation\n")
    
    for idx, lesson in enumerate(lessons_need_fix, 1):
        title_en = lesson['title']['en']
        desc_en = lesson['description']['en']
        content_en = lesson['content']['en'][:2000]
        
        print(f"[{idx}/{len(lessons_need_fix)}] Translating: {title_en[:50]}...")
        
        try:
            # Translate to Sinhala
            title_si = translator.translate(title_en, target_language='si', source_language='en')['translatedText']
            desc_si = translator.translate(desc_en, target_language='si', source_language='en')['translatedText']
            content_si = translator.translate(content_en, target_language='si', source_language='en')['translatedText']
            
            # Update
            await lessons_collection.update_one(
                {'id': lesson['id']},
                {'$set': {
                    'title.si': title_si,
                    'description.si': desc_si,
                    'content.si': content_si
                }}
            )
            print(f"  ✅ {title_si[:40]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Fixed {len(lessons_need_fix)} lessons!")
    client_motor.close()

if __name__ == '__main__':
    asyncio.run(fix_missing_sinhala())
