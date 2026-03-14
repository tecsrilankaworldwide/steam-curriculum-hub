#!/usr/bin/env python3
"""
Quick translation progress checker
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.getenv('DB_NAME', 'test_database')

client = MongoClient(mongo_url)
db = client[db_name]

# Count total AI lessons
total = db.lessons.count_documents({"is_ai_curriculum": True})

# Count lessons with translations
si_count = db.lessons.count_documents({
    "is_ai_curriculum": True,
    "title.si": {"$exists": True, "$ne": None, "$ne": ""}
})

ta_count = db.lessons.count_documents({
    "is_ai_curriculum": True,
    "title.ta": {"$exists": True, "$ne": None, "$ne": ""}
})

zh_count = db.lessons.count_documents({
    "is_ai_curriculum": True,
    "title.zh": {"$exists": True, "$ne": None, "$ne": ""}
})

yue_count = db.lessons.count_documents({
    "is_ai_curriculum": True,
    "title.yue": {"$exists": True, "$ne": None, "$ne": ""}
})

print(f"\n{'='*60}")
print(f"📊 TRANSLATION PROGRESS REPORT")
print(f"{'='*60}")
print(f"Total AI Lessons: {total}")
print(f"")
print(f"Round 1 (GPT-5.2):")
print(f"  ✅ Sinhala (si):   {si_count:4d}/{total} ({si_count/total*100:5.1f}%)")
print(f"  ✅ Tamil (ta):     {ta_count:4d}/{total} ({ta_count/total*100:5.1f}%)")
print(f"")
print(f"Round 2 (GPT-4o-mini):")
print(f"  ✅ Mandarin (zh):  {zh_count:4d}/{total} ({zh_count/total*100:5.1f}%)")
print(f"  ✅ Cantonese (yue): {yue_count:4d}/{total} ({yue_count/total*100:5.1f}%)")
print(f"{'='*60}")

# Calculate pending
round1_complete = min(si_count, ta_count)
round2_complete = min(zh_count, yue_count)

print(f"\n🎯 Status:")
print(f"  Round 1: {round1_complete}/{total} complete ({total - round1_complete} pending)")
print(f"  Round 2: {round2_complete}/{total} complete ({total - round2_complete} pending)")
print(f"\n")

client.close()
