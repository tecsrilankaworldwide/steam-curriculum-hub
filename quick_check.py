#!/usr/bin/env python3
"""
Quick script to check translation progress
Usage: python3 quick_check.py
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

async def check():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    langs = [
        ('si', '🇱🇰 Sinhala'), ('ta', '🇮🇳 Tamil'),
        ('hi', '🇮🇳 Hindi'), ('bn', '🇧🇩 Bengali'), ('mr', '🇮🇳 Marathi'),
        ('te', '🇮🇳 Telugu'), ('th', '🇹🇭 Thai'), ('tl', '🇵🇭 Filipino'),
        ('ms', '🇲🇾 Malay'), ('zh', '🇨🇳 Mandarin'), ('yue', '🇭🇰 Cantonese')
    ]
    
    print("\n" + "="*60)
    print("📊 TRANSLATION PROGRESS - LIVE STATUS")
    print("="*60)
    
    completed = 0
    in_progress = 0
    
    for code, name in langs:
        cnt = await db.lessons.count_documents({f"title.{code}": {"$exists": True, "$ne": ""}})
        pct = cnt/10
        
        if cnt >= 990:
            status = "✅ COMPLETE"
            completed += 1
        elif cnt > 50:
            status = "🔄 IN PROGRESS"
            in_progress += 1
        else:
            status = "⏳ STARTING"
        
        bar_length = int(pct / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        print(f"{name:20} {bar} {cnt:4}/1000 ({pct:5.1f}%) {status}")
    
    print("="*60)
    print(f"✅ Completed: {completed}/11 languages")
    print(f"🔄 In Progress: {in_progress}/11 languages")
    print(f"⏳ Pending: {11 - completed - in_progress}/11 languages")
    print("="*60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check())
