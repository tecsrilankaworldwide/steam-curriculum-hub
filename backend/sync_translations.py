"""
Periodic sync of translated lessons from Atlas to local MongoDB
Run this in background to keep the preview up-to-date
"""
import asyncio
import time
from motor.motor_asyncio import AsyncIOMotorClient

ATLAS_URL = "mongodb+srv://tecadmin:Niranjan1963@cluster0.0cisjyt.mongodb.net/steam_hub?retryWrites=true&w=majority"
LOCAL_URL = "mongodb://localhost:27017"
DB_NAME = "steam_hub"
SYNC_INTERVAL = 120  # seconds

async def sync_once():
    atlas = AsyncIOMotorClient(ATLAS_URL)
    local = AsyncIOMotorClient(LOCAL_URL)
    
    translated = await atlas[DB_NAME].lessons.find(
        {'translations_complete': True}
    ).to_list(length=1100)
    
    synced = 0
    for lesson in translated:
        lid = lesson.get('id')
        if lid:
            if '_id' in lesson:
                del lesson['_id']
            await local[DB_NAME].lessons.update_one(
                {'id': lid}, {'$set': lesson}, upsert=True
            )
            synced += 1
    
    local_count = await local[DB_NAME].lessons.count_documents({'translations_complete': True})
    
    atlas.close()
    local.close()
    
    return synced, local_count

async def main():
    print("🔄 Starting periodic Atlas → Local sync...")
    print(f"⏰ Interval: every {SYNC_INTERVAL}s\n")
    
    while True:
        try:
            synced, total = await sync_once()
            print(f"[{time.strftime('%H:%M:%S')}] Synced {synced} lessons. Local: {total} translated")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Sync error: {e}")
        
        await asyncio.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
