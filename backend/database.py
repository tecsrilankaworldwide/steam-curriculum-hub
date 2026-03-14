from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ.get('DB_NAME', 'steam_hub')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Collections
users_collection = db.users
lessons_collection = db.lessons
quizzes_collection = db.quizzes
progress_collection = db.progress
inquiries_collection = db.inquiries
certificates_collection = db.certificates

# Helper function to serialize MongoDB documents
def serialize_doc(doc):
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    if isinstance(doc, dict):
        doc = dict(doc)
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        # Handle nested dicts
        for key, value in doc.items():
            if isinstance(value, dict) or isinstance(value, list):
                doc[key] = serialize_doc(value)
        return doc
    return doc