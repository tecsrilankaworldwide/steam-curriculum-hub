"""
Load all 1000 AI lessons into MongoDB
"""

import asyncio
import json
import glob
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Get the directory where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load .env from script directory
load_dotenv(os.path.join(SCRIPT_DIR, '.env'))

async def load_all_lessons():
    # Connect to MongoDB using environment variable
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.getenv('DB_NAME', 'steam_hub')
    
    print(f"🔗 Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    lessons_collection = db.lessons
    
    # Find all AI lesson batch files in script directory
    batch_pattern = os.path.join(SCRIPT_DIR, 'ai_lessons_batch_*.json')
    batch_files = sorted(glob.glob(batch_pattern))
    
    print(f"🚀 Found {len(batch_files)} batch files to load")
    print(f"📁 Files: {[f.split('/')[-1] for f in batch_files]}\n")
    
    total_loaded = 0
    
    for batch_file in batch_files:
        print(f"📥 Loading {batch_file.split('/')[-1]}...")
        
        with open(batch_file, 'r', encoding='utf-8') as f:
            lessons = json.load(f)
        
        # Add multimedia and metadata
        for lesson in lessons:
            lesson['media'] = {
                'videos': get_educational_videos(lesson['age_group']),
                'images': [
                    "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
                    "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800"
                ]
            }
            lesson['is_ai_curriculum'] = True
            lesson['version'] = '2.0'
        
        # Insert batch
        result = await lessons_collection.insert_many(lessons)
        total_loaded += len(result.inserted_ids)
        
        print(f"  ✅ Loaded {len(result.inserted_ids)} lessons (Total: {total_loaded})\n")
    
    # Get final stats
    total_count = await lessons_collection.count_documents({})
    ai_count = await lessons_collection.count_documents({'is_ai_curriculum': True})
    traditional = total_count - ai_count
    
    print(f"{'='*60}")
    print(f"🎉 ALL LESSONS LOADED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"📊 Database Statistics:")
    print(f"   Total Lessons: {total_count}")
    print(f"   AI Curriculum: {ai_count}")
    print(f"   Traditional (Math/Physics): {traditional}")
    print(f"{'='*60}\n")
    
    client.close()

def get_educational_videos(age_group):
    """Get relevant educational video links"""
    video_map = {
        "5-7": ["https://www.youtube.com/watch?v=kWmX3pd1f10"],
        "8-9": ["https://www.youtube.com/watch?v=aircAruvnKk"],
        "10-12": ["https://www.youtube.com/watch?v=aircAruvnKk"],
        "13-15": ["https://www.youtube.com/watch?v=aircAruvnKk"],
        "16-18": ["https://www.youtube.com/watch?v=aircAruvnKk"]
    }
    return video_map.get(age_group, [])

if __name__ == "__main__":
    asyncio.run(load_all_lessons())
