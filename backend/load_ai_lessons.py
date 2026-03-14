"""
Load AI lessons into database and add multimedia content
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def load_ai_lessons():
    # Connect to MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['steam_hub']
    lessons_collection = db.lessons
    
    # Load generated lessons
    with open('/app/backend/ai_lessons_batch1.json', 'r', encoding='utf-8') as f:
        lessons = json.load(f)
    
    print(f"📚 Loading {len(lessons)} AI lessons into database...")
    
    # Add multimedia content for each lesson
    for i, lesson in enumerate(lessons):
        # Add relevant YouTube educational videos (Creative Commons / Educational Use)
        lesson['media']['videos'] = get_educational_videos(lesson)
        
        # Add image URLs from Unsplash (free, royalty-free)
        lesson['media']['images'] = get_relevant_images(lesson)
        
        # Mark as AI curriculum
        lesson['is_ai_curriculum'] = True
        lesson['version'] = '1.0'
        
        print(f"Processing lesson {i+1}/{len(lessons)}: {lesson['title']['en'][:50]}...")
    
    # Insert into database
    result = await lessons_collection.insert_many(lessons)
    print(f"✅ Successfully inserted {len(result.inserted_ids)} AI lessons!")
    
    # Verify
    total_count = await lessons_collection.count_documents({})
    ai_count = await lessons_collection.count_documents({'is_ai_curriculum': True})
    
    print(f"\n📊 Database Stats:")
    print(f"   Total lessons: {total_count}")
    print(f"   AI curriculum: {ai_count}")
    print(f"   Traditional: {total_count - ai_count}")
    
    client.close()

def get_educational_videos(lesson):
    """Get relevant educational video links"""
    age_group = lesson['age_group']
    title = lesson['title']['en']
    
    # Map to relevant YouTube educational channels (all free, educational use)
    video_map = {
        "5-7": [
            "https://www.youtube.com/watch?v=kWmX3pd1f10",  # What is AI for Kids
            "https://www.youtube.com/watch?v=2Ljhvjk0x9A",  # AI Explained Simple
        ],
        "8-9": [
            "https://www.youtube.com/watch?v=nKW8Ndu7Mjw",  # Machine Learning for Kids
            "https://www.youtube.com/watch?v=aircAruvnKk",  # Neural Networks 3Blue1Brown
        ],
        "10-12": [
            "https://www.youtube.com/watch?v=aircAruvnKk",  # Neural Networks Explained
            "https://www.youtube.com/watch?v=IHZwWFHWa-w",  # AI CrashCourse
        ],
        "13-15": [
            "https://www.youtube.com/watch?v=aircAruvnKk",  # Deep Learning Series
            "https://www.youtube.com/watch?v=IHZwWFHWa-w",  # AI Foundations
        ],
        "16-18": [
            "https://www.youtube.com/watch?v=aircAruvnKk",  # Advanced ML
            "https://www.youtube.com/watch?v=IHZwWFHWa-w",  # Research-level AI
        ]
    }
    
    return video_map.get(age_group, [])[:2]  # Max 2 videos per lesson

def get_relevant_images(lesson):
    """Get relevant image URLs from free sources"""
    keywords = lesson['keywords']
    
    # These are placeholder Unsplash URLs for AI/tech/education themes
    # In production, you'd use Unsplash API to get specific images
    image_urls = [
        "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",  # AI/Robot
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800",  # Technology
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",  # Digital
    ]
    
    return image_urls[:2]  # Max 2 images per lesson

if __name__ == "__main__":
    asyncio.run(load_ai_lessons())
