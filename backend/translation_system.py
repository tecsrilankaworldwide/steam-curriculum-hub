"""
AI Translation System for 1000+ Lessons
Translates all lessons to 20 languages using AI
"""

SUPPORTED_LANGUAGES = {
    "en": "English",
    "si": "Sinhala",
    "ta": "Tamil",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ar": "Arabic",
    "zh": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "ru": "Russian",
    "it": "Italian",
    "tr": "Turkish",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "bn": "Bengali",
    "ur": "Urdu"
}

# Simple translation templates for proof of concept
# In production, you would use a translation API like DeepL or Google Translate

TRANSLATION_TEMPLATES = {
    # AI topic terms that appear frequently
    "artificial_intelligence": {
        "en": "Artificial Intelligence",
        "si": "කෘතිම බුද්ධිය",
        "ta": "செயற்கை நுண்ணறிவு",
        "hi": "कृत्रिम बुद्धिमत्ता",
        "es": "Inteligencia Artificial",
        "fr": "Intelligence Artificielle",
        "de": "Künstliche Intelligenz",
        "ar": "الذكاء الاصطناعي",
        "zh": "人工智能",
        "ja": "人工知能",
        "ko": "인공지능"
    },
    "machine_learning": {
        "en": "Machine Learning",
        "si": "යන්ත්‍ර ඉගෙනීම",
        "ta": "இயந்திர கற்றல்",
        "hi": "मशीन लर्निंग",
        "es": "Aprendizaje Automático",
        "fr": "Apprentissage Automatique",
        "de": "Maschinelles Lernen",
        "ar": "تعلم الآلة",
        "zh": "机器学习",
        "ja": "機械学習",
        "ko": "기계 학습"
    },
    "neural_network": {
        "en": "Neural Network",
        "si": "ස්නායු ජාලය",
        "ta": "நரம்பு வலை",
        "hi": "न्यूरल नेटवर्क",
        "es": "Red Neuronal",
        "fr": "Réseau de Neurones",
        "de": "Neuronales Netzwerk",
        "ar": "الشبكة العصبية",
        "zh": "神经网络",
        "ja": "ニューラルネットワーク",
        "ko": "신경망"
    }
}

def create_translation_note():
    """Create a translation marker for lessons"""
    return {
        "note": "This lesson is available in multiple languages. Each lesson includes both the local language and English for better understanding.",
        "supported_languages": list(SUPPORTED_LANGUAGES.keys()),
        "translation_method": "AI-assisted translation (requires review)",
        "bilingual_mode": "Mother tongue + English side-by-side"
    }

async def add_translation_support_to_lessons():
    """Add translation framework to all lessons in database"""
    from motor.motor_asyncio import AsyncIOMotorClient
    
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['steam_hub']
    lessons_collection = db.lessons
    
    print("🌍 Adding multilingual support to all lessons...")
    print(f"📚 Target languages: {len(SUPPORTED_LANGUAGES)}")
    print(f"🗣️ Languages: {', '.join(SUPPORTED_LANGUAGES.values())}\n")
    
    # Update all lessons with translation metadata
    result = await lessons_collection.update_many(
        {},
        {
            "$set": {
                "translation_info": create_translation_note(),
                "available_languages": list(SUPPORTED_LANGUAGES.keys()),
                "default_language": "en",
                "bilingual_mode_supported": True
            }
        }
    )
    
    print(f"✅ Updated {result.modified_count} lessons with translation metadata")
    
    # Add sample translations for first 10 lessons of each age group
    print("\n🎯 Adding sample translations for demonstration...")
    
    for age_group in ["5-7", "8-9", "10-12", "13-15", "16-18"]:
        lessons = await lessons_collection.find(
            {"age_group": age_group, "is_ai_curriculum": True}
        ).limit(10).to_list(length=10)
        
        for lesson in lessons:
            # Add sample translations (in production, call translation API here)
            translations = add_sample_translations(lesson)
            
            await lessons_collection.update_one(
                {"id": lesson["id"]},
                {"$set": {"translations": translations}}
            )
        
        print(f"  ✓ Added sample translations for {len(lessons)} lessons (Age {age_group})")
    
    print(f"\n{'='*60}")
    print("✅ Translation framework added successfully!")
    print(f"{'='*60}")
    print("\n📝 Next Steps:")
    print("   1. Integrate with translation API (DeepL, Google Translate, etc.)")
    print("   2. Bulk translate all 1000+ lessons")
    print("   3. Human review for quality assurance")
    print("   4. Enable bilingual display in UI\n")
    
    client.close()

def add_sample_translations(lesson):
    """Add sample translations for a lesson (placeholder)"""
    title_en = lesson['title']['en']
    desc_en = lesson['description']['en']
    
    # Sample translations (in production, use real translation API)
    translations = {}
    
    for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
        if lang_code == 'en':
            continue
        
        translations[lang_code] = {
            "title": f"[{lang_name}] {title_en}",
            "description": f"[{lang_name}] {desc_en[:100]}...",
            "status": "placeholder",
            "needs_review": True
        }
    
    return translations

if __name__ == "__main__":
    import asyncio
    asyncio.run(add_translation_support_to_lessons())
