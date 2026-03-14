import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone
from auth import hash_password

# Get MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'steam_hub')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Comprehensive 80+ lessons for K-12
async def seed_comprehensive():
    print("🌱 Starting comprehensive database seeding for K-12 (ages 5-18)...")
    
    # Clear existing data
    print("Clearing existing data...")
    await db.lessons.delete_many({})
    await db.quizzes.delete_many({})
    await db.users.delete_many({})
    
    # Create admin and test student
    print("Creating users...")
    admin = {
        'id': str(uuid.uuid4()),
        'email': 'admin@steamhub.edu',
        'password_hash': hash_password('admin123'),
        'role': 'admin',
        'name': 'Admin User',
        'preferred_language': 'en-US',
        'display_mode': 'bilingual',
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    
    student = {
        'id': str(uuid.uuid4()),
        'email': 'student@test.com',
        'password_hash': hash_password('student123'),
        'role': 'student',
        'name': 'Test Student',
        'preferred_language': 'en-US',
        'display_mode': 'bilingual',
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    
    await db.users.insert_many([admin, student])
    print(f"✅ Users created: admin@steamhub.edu / admin123, student@test.com / student123")
    
    lessons = []
    
    # Mathematics lessons K-12
    math_topics = [
        ("K", "Counting Numbers 1-10", "Learn to count from 1 to 10", "गिनती 1-10 / Counting 1-10"),
        ("K", "Basic Shapes", "Identify circles, squares, triangles", "आकार / Shapes"),
        (1, "Addition Basics", "Adding single digit numbers", "जोड़ / Addition"),
        (1, "Subtraction Basics", "Subtracting single digit numbers", "घटाव / Subtraction"),
        (2, "Place Value", "Understanding tens and ones", "स्थानीय मान / Place Value"),
        (2, "Skip Counting", "Counting by 2s, 5s, and 10s", "छोड़कर गिनती / Skip Counting"),
        (3, "Multiplication Tables", "Times tables 1-10", "गुणन तालिका / Multiplication Tables"),
        (3, "Division Basics", "Introduction to division", "भाग / Division"),
        (4, "Fractions", "Understanding numerators and denominators", "भिन्न / Fractions"),
        (4, "Decimals", "Working with decimal numbers", "दशमलव / Decimals"),
        (5, "Percentages", "Converting fractions to percentages", "प्रतिशत / Percentages"),
        (5, "Geometry Basics", "Angles, perimeter, area", "ज्यामिति / Geometry"),
        (6, "Ratios and Proportions", "Understanding ratios", "अनुपात / Ratios"),
        (6, "Integers", "Positive and negative numbers", "पूर्णांक / Integers"),
        (7, "Algebraic Expressions", "Variables and expressions", "बीजगणितीय व्यंजक / Algebra"),
        (7, "Linear Equations", "Solving for x", "रैखिक समीकरण / Linear Equations"),
        (8, "Pythagorean Theorem", "Right triangles and squares", "पाइथागोरस प्रमेय / Pythagorean Theorem"),
        (8, "Probability", "Calculating chances", "प्रायिकता / Probability"),
        (9, "Quadratic Equations", "Solving ax² + bx + c = 0", "द्विघात समीकरण / Quadratic Equations"),
        (9, "Statistics", "Mean, median, mode", "सांख्यिकी / Statistics"),
        (10, "Trigonometry", "Sine, cosine, tangent", "त्रिकोणमिति / Trigonometry"),
        (10, "Functions", "Domain, range, graphing", "फलन / Functions"),
        (11, "Calculus Intro", "Limits and derivatives", "कलन / Calculus"),
        (11, "Matrices", "Matrix operations", "आव्यूह / Matrices"),
        (12, "Integration", "Area under curves", "समाकलन / Integration"),
        (12, "Complex Numbers", "Imaginary and real parts", "सम्मिश्र संख्याएँ / Complex Numbers")
    ]
    
    for curriculum in ['cambridge', 'edexcel', 'asdn']:
        for grade, title_en, desc_en, title_local in math_topics:
            lesson_id = str(uuid.uuid4())
            lesson = {
                'id': lesson_id,
                'title': {'en': title_en, 'local': title_local},
                'description': {'en': desc_en, 'local': f'{desc_en} का विवरण / Description of {desc_en}'},
                'content': {'en': f'Comprehensive content for {title_en}. This lesson covers fundamental concepts with examples and practice problems.', 
                           'local': f'{title_en} के लिए व्यापक सामग्री। यह पाठ उदाहरणों के साथ मौलिक अवधारणाओं को शामिल करता है।'},
                'curriculum': curriculum,
                'subject': 'mathematics',
                'grade': grade,
                'language_code': 'hi-IN',
                'difficulty': 'easy' if isinstance(grade, str) or grade <= 4 else 'medium' if grade <= 8 else 'hard',
                'estimated_duration': 30 + (0 if isinstance(grade, str) else grade * 2),
                'source': 'OpenStax',
                'license': 'CC BY 4.0',
                'source_url': 'https://openstax.org',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'updated_at': datetime.now(timezone.utc).isoformat()
            }
            lessons.append(lesson)
            
            # Create quiz
            quiz = {
                'id': str(uuid.uuid4()),
                'lesson_id': lesson_id,
                'questions': [
                    {
                        'question': {'en': f'What is the main concept in {title_en}?', 'local': f'{title_en} में मुख्य अवधारणा क्या है?'},
                        'options': [
                            {'en': 'Core principle', 'local': 'मुख्य सिद्धांत'},
                            {'en': 'Secondary concept', 'local': 'द्वितीयक अवधारणा'},
                            {'en': 'Advanced theory', 'local': 'उन्नत सिद्धांत'},
                            {'en': 'None of these', 'local': 'इनमें से कोई नहीं'}
                        ],
                        'correct_answer': 0,
                        'explanation': {'en': 'The core principle is fundamental to this topic', 'local': 'मुख्य सिद्धांत इस विषय के लिए मौलिक है'},
                        'difficulty': 'easy'
                    },
                    {
                        'question': {'en': f'How do you apply {title_en}?', 'local': f'आप {title_en} को कैसे लागू करते हैं?'},
                        'options': [
                            {'en': 'Through practice', 'local': 'अभ्यास के माध्यम से'},
                            {'en': 'By memorizing', 'local': 'याद करके'},
                            {'en': 'By guessing', 'local': 'अनुमान लगाकर'},
                            {'en': 'Never use it', 'local': 'कभी उपयोग नहीं करें'}
                        ],
                        'correct_answer': 0,
                        'explanation': {'en': 'Practice is key to mastering this concept', 'local': 'इस अवधारणा में महारत हासिल करने के लिए अभ्यास महत्वपूर्ण है'},
                        'difficulty': 'medium'
                    }
                ],
                'passing_score': 70,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            await db.quizzes.insert_one(quiz)
    
    # Physics lessons (Grades 5-12)
    physics_topics = [
        (5, "Simple Machines", "Levers, pulleys, wheels"),
        (6, "Force and Motion", "Newton's laws"),
        (7, "Energy Types", "Kinetic and potential energy"),
        (8, "Electricity Basics", "Circuits and current"),
        (9, "Light and Sound", "Waves and reflection"),
        (10, "Magnetism", "Magnetic fields"),
        (11, "Thermodynamics", "Heat and temperature"),
        (12, "Quantum Physics", "Particle wave duality")
    ]
    
    for curriculum in ['cambridge', 'edexcel', 'asdn']:
        for grade, title_en, desc_en in physics_topics:
            lesson_id = str(uuid.uuid4())
            lesson = {
                'id': lesson_id,
                'title': {'en': title_en, 'local': f'{title_en} / भौतिकी'},
                'description': {'en': desc_en, 'local': f'{desc_en} / विवरण'},
                'content': {'en': f'Explore {title_en}: {desc_en}. Learn through experiments and real-world applications.', 
                           'local': f'{title_en} का अन्वेषण करें। प्रयोगों और वास्तविक दुनिया के अनुप्रयोगों के माध्यम से सीखें।'},
                'curriculum': curriculum,
                'subject': 'physics',
                'grade': grade,
                'language_code': 'hi-IN',
                'difficulty': 'medium' if grade <= 8 else 'hard',
                'estimated_duration': 40 + grade * 2,
                'source': 'CK-12',
                'license': 'CC BY-NC 3.0',
                'source_url': 'https://ck12.org',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'updated_at': datetime.now(timezone.utc).isoformat()
            }
            lessons.append(lesson)
            
            # Create quiz
            quiz = {
                'id': str(uuid.uuid4()),
                'lesson_id': lesson_id,
                'questions': [
                    {
                        'question': {'en': f'What is {title_en}?', 'local': f'{title_en} क्या है?'},
                        'options': [
                            {'en': desc_en, 'local': f'{desc_en} / विवरण'},
                            {'en': 'Something else', 'local': 'कुछ और'},
                            {'en': 'Not physics', 'local': 'भौतिकी नहीं'},
                            {'en': 'Unknown', 'local': 'अज्ञात'}
                        ],
                        'correct_answer': 0,
                        'explanation': {'en': f'{title_en} is about {desc_en}', 'local': 'यह सही उत्तर है'},
                        'difficulty': 'medium'
                    }
                ],
                'passing_score': 70,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            await db.quizzes.insert_one(quiz)
    
    print(f"📚 Inserting {len(lessons)} lessons...")
    if lessons:
        await db.lessons.insert_many(lessons)
    
    print(f"✅ Database seeded successfully!")
    print(f"   Total lessons: {len(lessons)}")
    print(f"   Curricula: Cambridge, Edexcel, ASDN")
    print(f"   Grades: K-12 (ages 5-18)")
    print(f"   Subjects: Mathematics, Physics")
    print(f"   Admin: admin@steamhub.edu / admin123")
    print(f"   Student: student@test.com / student123")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_comprehensive())
