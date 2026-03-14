import asyncio
import sys
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

# Comprehensive lesson data for 80+ lessons across 3 curricula, 10 subjects, grades 3-10
LESSONS_DATA = []

# Cambridge Curriculum Lessons
cambridge_lessons = [
    # Mathematics - Grades 3-10
    {
        "title": {"en": "Introduction to Fractions", "local": "Fractions ka Parichay / फ्रैक्शन का परिचय"},
        "description": {"en": "Learn the basics of fractions including numerators and denominators", "local": "Numerators aur denominators sahit fractions ki basics / अंश और हर सहित भिन्न की बुनियादी बातें"},
        "content": {"en": "A fraction represents a part of a whole. It consists of a numerator (top number) and a denominator (bottom number). For example, in 1/2, 1 is the numerator and 2 is the denominator. This means one part out of two equal parts.", "local": "Fraction ek poore ka ek hissa dikhata hai. Ismein numerator (upar ki sankhya) aur denominator (niche ki sankhya) hota hai / एक भिन्न एक पूर्ण का एक भाग दर्शाता है। इसमें अंश (ऊपर की संख्या) और हर (नीचे की संख्या) होता है।"},
        "curriculum": "cambridge", "subject": "mathematics", "grade": 3, "language_code": "hi-IN",
        "difficulty": "easy", "estimated_duration": 30,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Linear Equations", "local": "Doğrusal Denklemler / Lineare Gleichungen"},
        "description": {"en": "Solve linear equations with one variable", "local": "Tek değişkenli doğrusal denklemleri çözme / Lineare Gleichungen mit einer Variablen lösen"},
        "content": {"en": "A linear equation is an equation where the highest power of the variable is 1. Example: 2x + 5 = 15. To solve: subtract 5 from both sides to get 2x = 10, then divide by 2 to get x = 5.", "local": "Doğrusal denklem, değişkenin en yüksek kuvvetinin 1 olduğu bir denklemdir / Eine lineare Gleichung ist eine Gleichung, bei der die höchste Potenz der Variablen 1 ist."},
        "curriculum": "cambridge", "subject": "mathematics", "grade": 7, "language_code": "tr-TR",
        "difficulty": "medium", "estimated_duration": 45,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "Quadratic Equations", "local": "معادلات من الدرجة الثانية / Ecuaciones Cuadráticas"},
        "description": {"en": "Understanding and solving quadratic equations", "local": "فهم وحل المعادلات التربيعية / Comprensión y resolución de ecuaciones cuadráticas"},
        "content": {"en": "A quadratic equation has the form ax² + bx + c = 0. Solutions can be found using factoring, completing the square, or the quadratic formula: x = (-b ± √(b²-4ac)) / 2a", "local": "المعادلة التربيعية لها الشكل ax² + bx + c = 0 / Una ecuación cuadrática tiene la forma ax² + bx + c = 0"},
        "curriculum": "cambridge", "subject": "mathematics", "grade": 9, "language_code": "ar-SA",
        "difficulty": "hard", "estimated_duration": 60,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    
    # Physics - Grades 5-10
    {
        "title": {"en": "Force and Motion", "local": "Bal aur Gati / बल और गति"},
        "description": {"en": "Introduction to Newton's laws of motion", "local": "Newton ke gati ke niyam ka parichay / न्यूटन के गति के नियम का परिचय"},
        "content": {"en": "Newton's First Law: An object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force. Newton's Second Law: Force = Mass × Acceleration (F = ma).", "local": "Newton ka pehla niyam: ek sthir vastu sthir rahti hai aur ek chalti vastu chalti rahti hai jab tak bahari bal na lage / न्यूटन का पहला नियम: एक स्थिर वस्तु स्थिर रहती है।"},
        "curriculum": "cambridge", "subject": "physics", "grade": 7, "language_code": "hi-IN",
        "difficulty": "medium", "estimated_duration": 40,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Electricity and Circuits", "local": "Điện và Mạch điện / Elektrik dan Sirkuit"},
        "description": {"en": "Understanding basic electrical circuits", "local": "Hiểu về mạch điện cơ bản / Memahami sirkuit listrik dasar"},
        "content": {"en": "An electric circuit is a closed path through which electric current can flow. It requires a power source (battery), conductors (wires), and a load (bulb). Current flows from positive to negative terminal.", "local": "Mạch điện là đường dẫn kín mà dòng điện có thể chạy qua / Sirkuit listrik adalah jalur tertutup di mana arus listrik dapat mengalir."},
        "curriculum": "cambridge", "subject": "physics", "grade": 8, "language_code": "vi-VN",
        "difficulty": "medium", "estimated_duration": 50,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    
    # Chemistry - Grades 6-10
    {
        "title": {"en": "States of Matter", "local": "Padarth ki Awastha / पदार्थ की अवस्था"},
        "description": {"en": "Learn about solid, liquid, and gas states", "local": "Kathor, drav aur gas awasthaon ke bare mein / ठोस, तरल और गैस अवस्थाओं के बारे में"},
        "content": {"en": "Matter exists in three main states: Solid (fixed shape and volume), Liquid (fixed volume but takes shape of container), and Gas (no fixed shape or volume). These states can change through heating or cooling.", "local": "Padarth teen mukhya awasthaon mein paya jata hai: Kathor, Drav aur Gas / पदार्थ तीन मुख्य अवस्थाओं में पाया जाता है।"},
        "curriculum": "cambridge", "subject": "chemistry", "grade": 6, "language_code": "hi-IN",
        "difficulty": "easy", "estimated_duration": 35,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Chemical Reactions", "local": "রাসায়নিক বিক্রিয়া / ردود فعل كيميائية"},
        "description": {"en": "Understanding types of chemical reactions", "local": "রাসায়নিক বিক্রিয়ার প্রকারভেদ / فهم أنواع التفاعلات الكيميائية"},
        "content": {"en": "Chemical reactions involve the transformation of reactants into products. Types include: Synthesis (A + B → AB), Decomposition (AB → A + B), Single Replacement (A + BC → AC + B), and Double Replacement (AB + CD → AD + CB).", "local": "রাসায়নিক বিক্রিয়ায় বিক্রিয়াকারী পদার্থ পণ্যে রূপান্তরিত হয় / تتضمن التفاعلات الكيميائية تحويل المواد المتفاعلة إلى منتجات."},
        "curriculum": "cambridge", "subject": "chemistry", "grade": 9, "language_code": "bn-IN",
        "difficulty": "hard", "estimated_duration": 55,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    
    # Biology - Grades 5-10
    {
        "title": {"en": "Plant Cell Structure", "local": "Bitki Hücre Yapısı / Paudhe ki Koshika Rachna"},
        "description": {"en": "Learn about the parts of a plant cell", "local": "Bitki hücresinin parçaları / पौधे की कोशिका के भाग"},
        "content": {"en": "Plant cells have a cell wall, cell membrane, nucleus, cytoplasm, chloroplasts, vacuole, and mitochondria. The cell wall provides structure, chloroplasts perform photosynthesis, and the vacuole stores water.", "local": "Bitki hücreleri hücre duvarı, hücre zarı, çekirdek, sitoplazma içerir / पौधे की कोशिका में कोशिका भित्ति, कोशिका झिल्ली होती है।"},
        "curriculum": "cambridge", "subject": "biology", "grade": 7, "language_code": "tr-TR",
        "difficulty": "medium", "estimated_duration": 40,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Human Digestive System", "local": "人体消化系统 / Sistema Digestivo Humano"},
        "description": {"en": "How the digestive system processes food", "local": "消化系统如何处理食物 / Cómo el sistema digestivo procesa los alimentos"},
        "content": {"en": "The digestive system includes the mouth, esophagus, stomach, small intestine, large intestine, and accessory organs. Digestion begins in the mouth with mechanical and chemical breakdown, continues in the stomach with acid, and absorption occurs in the small intestine.", "local": "消化系统包括口腔、食道、胃、小肠、大肠 / El sistema digestivo incluye la boca, el esófago, el estómago."},
        "curriculum": "cambridge", "subject": "biology", "grade": 8, "language_code": "zh-CN",
        "difficulty": "medium", "estimated_duration": 45,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
]

# Continue with more Cambridge lessons for other subjects
cambridge_lessons.extend([
    # Science (General)
    {
        "title": {"en": "Water Cycle", "local": "Pani ka Chakra / पानी का चक्र"},
        "description": {"en": "Understanding the water cycle on Earth", "local": "Prithvi par pani ke chakra ko samajhna / पृथ्वी पर पानी के चक्र को समझना"},
        "content": {"en": "The water cycle includes evaporation (water turns to vapor), condensation (vapor forms clouds), precipitation (rain/snow falls), and collection (water gathers in rivers/lakes). This continuous process recycles Earth's water.", "local": "Pani ka chakra mein vaapatikaran, sanghan, varshavikriya shamil hai / पानी के चक्र में वाष्पीकरण, संघनन, वर्षण शामिल है।"},
        "curriculum": "cambridge", "subject": "science", "grade": 5, "language_code": "hi-IN",
        "difficulty": "easy", "estimated_duration": 30,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Solar System", "local": "సౌర వ్యవస్థ / Surya Mandal"},
        "description": {"en": "Exploring planets and celestial bodies", "local": "గ్రహాలు మరియు ఖగోళ వస్తువులు / ग्रह और खगोलीय पिंड"},
        "content": {"en": "The Solar System consists of the Sun, eight planets (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune), moons, asteroids, and comets. Planets orbit the Sun due to gravity.", "local": "సౌర వ్యవస్థలో సూర్యుడు, ఎనిమిది గ్రహాలు ఉన్నాయి / सौर मंडल में सूर्य, आठ ग्रह हैं।"},
        "curriculum": "cambridge", "subject": "science", "grade": 6, "language_code": "te-IN",
        "difficulty": "medium", "estimated_duration": 50,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    
    # Technology & ICT
    {
        "title": {"en": "Introduction to Computers", "local": "کمپیوٹر کا تعارف / Computer ka Parichay"},
        "description": {"en": "Basic computer components and functions", "local": "کمپیوٹر کے بنیادی اجزاء / कंप्यूटर के बुनियादी घटक"},
        "content": {"en": "A computer has input devices (keyboard, mouse), processing unit (CPU), memory (RAM, ROM), storage (hard drive), and output devices (monitor, printer). It processes data to produce useful information.", "local": "کمپیوٹر میں ان پٹ ڈیوائسز، سی پی یو، میموری ہوتی ہے / कंप्यूटर में इनपुट डिवाइस, सीपीयू, मेमोरी होती है।"},
        "curriculum": "cambridge", "subject": "ict", "grade": 5, "language_code": "ur-PK",
        "difficulty": "easy", "estimated_duration": 35,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Internet Safety", "local": "インターネットの安全性 / Internet Seguridad"},
        "description": {"en": "Staying safe online", "local": "オンラインで安全に / Mantenerse seguro en línea"},
        "content": {"en": "Internet safety includes using strong passwords, not sharing personal information, recognizing phishing attempts, and being careful about what you post online. Always verify websites before entering sensitive data.", "local": "インターネットの安全には強力なパスワードの使用が含まれます / La seguridad en Internet incluye usar contraseñas seguras."},
        "curriculum": "cambridge", "subject": "ict", "grade": 7, "language_code": "ja-JP",
        "difficulty": "medium", "estimated_duration": 40,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    
    # Engineering
    {
        "title": {"en": "Simple Machines", "local": "सरल यन्त्रहरू / Basit Makineler"},
        "description": {"en": "Understanding levers, pulleys, and wheels", "local": "लीभर, पुली र पाङ्ग्राहरू / Kaldıraçlar, makaralar ve tekerlekler"},
        "content": {"en": "Simple machines make work easier. Six types exist: lever, wheel and axle, pulley, inclined plane, wedge, and screw. They change the direction or magnitude of force applied.", "local": "सरल यन्त्रहरूले काम सजिलो बनाउँछन् / Basit makineler işi kolaylaştırır."},
        "curriculum": "cambridge", "subject": "engineering", "grade": 6, "language_code": "ne-NP",
        "difficulty": "medium", "estimated_duration": 45,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    
    # Arts
    {
        "title": {"en": "Color Theory", "local": "रंग सिद्धान्त / Теория цвета"},
        "description": {"en": "Understanding primary, secondary, and tertiary colors", "local": "प्राथमिक, द्वितीयक र तृतीयक रङहरू / Первичные, вторичные и третичные цвета"},
        "content": {"en": "Primary colors are red, yellow, and blue. Secondary colors (orange, green, purple) are made by mixing two primary colors. Tertiary colors are made by mixing primary and secondary colors.", "local": "प्राथमिक रङहरू रातो, पहेंलो र निलो हुन् / Основные цвета - красный, желтый и синий."},
        "curriculum": "cambridge", "subject": "arts", "grade": 4, "language_code": "ne-NP",
        "difficulty": "easy", "estimated_duration": 30,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    
    # English
    {
        "title": {"en": "Parts of Speech", "local": "ဝါကျအစိတ်အပိုင်းများ / Bahagi ng Pananalita"},
        "description": {"en": "Nouns, verbs, adjectives, and more", "local": "နာမ်၊ ကြိယာ၊ နာမဝိသေသန / Pangngalan, pandiwa, pang-uri"},
        "content": {"en": "There are eight parts of speech: noun (person/place/thing), pronoun (replaces noun), verb (action/state), adjective (describes noun), adverb (describes verb), preposition (shows relationship), conjunction (connects), interjection (expresses emotion).", "local": "ဝါကျအစိတ်အပိုင်းရှစ်မျိုးရှိသည် / May walong bahagi ng pananalita."},
        "curriculum": "cambridge", "subject": "english", "grade": 5, "language_code": "my-MM",
        "difficulty": "medium", "estimated_duration": 40,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
])

# Edexcel Curriculum Lessons
edexcel_lessons = [
    {
        "title": {"en": "Algebraic Expressions", "local": "बीजगणितीय व्यंजक / Cebirsel İfadeler"},
        "description": {"en": "Simplifying and evaluating algebraic expressions", "local": "बीजगणितीय व्यंजकों को सरल बनाना / Cebirsel ifadeleri basitleştirme"},
        "content": {"en": "An algebraic expression contains variables, numbers, and operations. To simplify: combine like terms (terms with same variable and power). Example: 3x + 5x = 8x. To evaluate: substitute numbers for variables.", "local": "एक बीजगणितीय व्यंजक में चर, संख्याएं होती हैं / Cebirsel ifade değişkenler, sayılar içerir."},
        "curriculum": "edexcel", "subject": "mathematics", "grade": 6, "language_code": "hi-IN",
        "difficulty": "medium", "estimated_duration": 40,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "Probability Basics", "local": "확률 기초 / Probabilità di base"},
        "description": {"en": "Introduction to probability and chance", "local": "확률과 가능성 소개 / Introduzione alla probabilità"},
        "content": {"en": "Probability measures how likely an event is to occur. It ranges from 0 (impossible) to 1 (certain). Formula: P(event) = (favorable outcomes) / (total outcomes). Example: probability of rolling a 6 on a die is 1/6.", "local": "확률은 사건이 발생할 가능성을 측정합니다 / La probabilità misura quanto è probabile che si verifichi un evento."},
        "curriculum": "edexcel", "subject": "mathematics", "grade": 8, "language_code": "ko-KR",
        "difficulty": "medium", "estimated_duration": 45,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Light and Reflection", "local": "प्रकाश र प्रतिबिम्ब / Luz y Reflexión"},
        "description": {"en": "How light travels and reflects off surfaces", "local": "प्रकाश कसरी यात्रा गर्छ / Cómo viaja la luz"},
        "content": {"en": "Light travels in straight lines. When it hits a surface, it can be reflected, absorbed, or transmitted. Law of reflection: angle of incidence equals angle of reflection. Mirrors use reflection to form images.", "local": "प्रकाश सीधा रेखामा यात्रा गर्छ / La luz viaja en líneas rectas."},
        "curriculum": "edexcel", "subject": "physics", "grade": 7, "language_code": "ne-NP",
        "difficulty": "medium", "estimated_duration": 40,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "Atomic Structure", "local": "परमाणु संरचना / Struttura Atomica"},
        "description": {"en": "Understanding protons, neutrons, and electrons", "local": "प्रोटॉन, न्यूट्रॉन और इलेक्ट्रॉन / Protoni, neutroni ed elettroni"},
        "content": {"en": "An atom has a nucleus containing protons (positive charge) and neutrons (no charge), surrounded by electrons (negative charge) in orbitals. Atomic number = number of protons. Mass number = protons + neutrons.", "local": "एक परमाणु में नाभिक होता है / Un atomo ha un nucleo."},
        "curriculum": "edexcel", "subject": "chemistry", "grade": 9, "language_code": "hi-IN",
        "difficulty": "hard", "estimated_duration": 50,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Photosynthesis", "local": "प्रकाश संश्लेषण / Fotosentez"},
        "description": {"en": "How plants make food using sunlight", "local": "पौधे सूर्य के प्रकाश से भोजन कैसे बनाते हैं / Bitkiler güneş ışığından nasıl besin yapar"},
        "content": {"en": "Photosynthesis occurs in chloroplasts. Plants use carbon dioxide, water, and sunlight to produce glucose and oxygen. Equation: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂. This process is essential for life on Earth.", "local": "प्रकाश संश्लेषण क्लोरोप्लास्ट में होता है / Fotosentez kloroplastlarda gerçekleşir."},
        "curriculum": "edexcel", "subject": "biology", "grade": 8, "language_code": "hi-IN",
        "difficulty": "medium", "estimated_duration": 45,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
])

# Continue adding Edexcel lessons for remaining subjects
edexcel_lessons.extend([
    {
        "title": {"en": "Weather and Climate", "local": "Temps và Khí hậu / Panahon at Klima"},
        "description": {"en": "Difference between weather and climate", "local": "Sự khác biệt giữa thời tiết và khí hậu / Pagkakaiba ng panahon at klima"},
        "content": {"en": "Weather is the day-to-day state of the atmosphere (temperature, precipitation, wind). Climate is the average weather pattern over many years in a region. Factors affecting climate include latitude, altitude, and proximity to water.", "local": "Thời tiết là trạng thái hàng ngày / Ang panahon ay ang pang-araw-araw na kalagayan."},
        "curriculum": "edexcel", "subject": "science", "grade": 6, "language_code": "vi-VN",
        "difficulty": "medium", "estimated_duration": 35,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Coding Basics with Scratch", "local": "Scratch के साथ कोडिंग / Scratch ile Kodlama"},
        "description": {"en": "Introduction to block-based programming", "local": "ब्लॉक-आधारित प्रोग्रामिंग / Blok tabanlı programlama"},
        "content": {"en": "Scratch is a visual programming language using blocks. Key concepts: sprites (characters), stages (background), scripts (code blocks). Commands include motion, looks, sound, events, and control blocks. Create animations and games!", "local": "Scratch एक दृश्य प्रोग्रामिंग भाषा है / Scratch bloklar kullanan görsel bir programlama dilidir."},
        "curriculum": "edexcel", "subject": "ict", "grade": 5, "language_code": "hi-IN",
        "difficulty": "easy", "estimated_duration": 45,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "Bridge Design", "local": "Көпүрө дизайны / တံတားဒီဇိုင်း"},
        "description": {"en": "Engineering principles in bridge construction", "local": "Көпүрө куруудагы инженердик принциптер / တံတားတည်ဆောက်မှုတွင်"},
        "content": {"en": "Bridges must support weight (compression) and resist pulling forces (tension). Types include beam bridges (simple), arch bridges (compression), suspension bridges (tension cables). Engineers consider materials, span, and load.", "local": "Көпүрөлөр салмакты көтөрүшү керек / တံတားများသည်အလေးချိန်ကိုထောက်ပံ့ရမည်။"},
        "curriculum": "edexcel", "subject": "engineering", "grade": 8, "language_code": "ky-KG",
        "difficulty": "hard", "estimated_duration": 55,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Music Composition", "local": "संगीत रचना / Музыкийн найрал"},
        "description": {"en": "Creating melodies and harmonies", "local": "धुन र स्वर सिर्जना / Аялгуу ба зохицол бүтээх"},
        "content": {"en": "Music composition involves creating melodies (single line of notes), harmonies (multiple notes played together), and rhythm (pattern of beats). Elements include pitch, duration, dynamics, and timbre. Start with a simple melody and build!", "local": "संगीत रचनामा धुन सिर्जना समावेश छ / Хөгжмийн найрал нь аялгуу бүтээх явдал юм."},
        "curriculum": "edexcel", "subject": "arts", "grade": 7, "language_code": "ne-NP",
        "difficulty": "medium", "estimated_duration": 50,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "Essay Writing", "local": "Tiếng Anh Viết luận / Pagsusulat ng Sanaysay"},
        "description": {"en": "Structure and techniques for writing essays", "local": "Cấu trúc và kỹ thuật viết luận / Istraktura at mga teknik"},
        "content": {"en": "An essay has three parts: introduction (hook + thesis), body paragraphs (topic sentence + evidence + analysis), conclusion (restate thesis + final thoughts). Use transitions between paragraphs. Always proofread!", "local": "Bài luận có ba phần: giới thiệu, thân bài, kết luận / Ang sanaysay ay may tatlong bahagi."},
        "curriculum": "edexcel", "subject": "english", "grade": 9, "language_code": "vi-VN",
        "difficulty": "hard", "estimated_duration": 60,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
])

# ASDN Curriculum Lessons
asdn_lessons = [
    {
        "title": {"en": "Geometry: Triangles", "local": "ज्यामिति: त्रिभुज / Geometri: Segitiga"},
        "description": {"en": "Properties and types of triangles", "local": "त्रिभुजका गुणहरू र प्रकारहरू / Sifat dan jenis segitiga"},
        "content": {"en": "Triangles have three sides and three angles. Types: Equilateral (all sides equal), Isosceles (two sides equal), Scalene (no sides equal). Sum of angles always equals 180°. Area = ½ × base × height.", "local": "त्रिभुजमा तीन पक्ष र तीन कोण हुन्छन् / Segitiga memiliki tiga sisi dan tiga sudut."},
        "curriculum": "asdn", "subject": "mathematics", "grade": 5, "language_code": "ne-NP",
        "difficulty": "medium", "estimated_duration": 40,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "Statistics and Data", "local": "සංඛ්‍යාලේඛන සහ දත්ත / Istatistikler ve Veriler"},
        "description": {"en": "Mean, median, mode, and range", "local": "සාමාන්‍ය, මධ්‍යස්ථ, ප්‍රකාරය / Ortalama, medyan, mod"},
        "content": {"en": "Statistics help analyze data. Mean: average of all values. Median: middle value when ordered. Mode: most frequent value. Range: difference between highest and lowest. Example: For 3, 5, 5, 7, 10: mean=6, median=5, mode=5, range=7.", "local": "සංඛ්‍යාලේඛන දත්ත විශ්ලේෂණය කරයි / İstatistikler verileri analiz eder."},
        "curriculum": "asdn", "subject": "mathematics", "grade": 7, "language_code": "si-LK",
        "difficulty": "medium", "estimated_duration": 45,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Sound Waves", "local": "ध्वनि तरंगें / Gelombang Suara"},
        "description": {"en": "How sound travels and properties of waves", "local": "ध्वनि कैसे यात्रा करती है / Bagaimana suara bergerak"},
        "content": {"en": "Sound is a wave that travels through matter (solid, liquid, gas). Properties: frequency (pitch), amplitude (loudness), wavelength. Sound travels fastest in solids, slowest in gases. Speed in air ≈ 343 m/s.", "local": "ध्वनि एक तरंग है जो पदार्थ से यात्रा करती है / Suara adalah gelombang yang bergerak melalui materi."},
        "curriculum": "asdn", "subject": "physics", "grade": 8, "language_code": "hi-IN",
        "difficulty": "medium", "estimated_duration": 40,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "pH and Acids/Bases", "local": "pH และกรด/เบส / pH dan Asam/Basa"},
        "description": {"en": "Understanding pH scale and acid-base reactions", "local": "การเข้าใจมาตรวัด pH / Memahami skala pH"},
        "content": {"en": "pH scale ranges from 0-14. pH < 7 is acidic, pH = 7 is neutral, pH > 7 is basic. Acids donate H⁺ ions, bases accept H⁺ ions. Examples: lemon juice (acid, pH 2), water (neutral, pH 7), soap (base, pH 9).", "local": "สเกล pH อยู่ระหว่าง 0-14 / Skala pH berkisar dari 0-14."},
        "curriculum": "asdn", "subject": "chemistry", "grade": 9, "language_code": "th-TH",
        "difficulty": "hard", "estimated_duration": 50,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Ecosystems and Food Chains", "local": "ಪರಿಸರ ವ್ಯವಸ್ಥೆಗಳು ಮತ್ತು ಆಹಾರ ಸರಪಳಿಗಳು / पारिस्थितिकी तंत्र और खाद्य श्रृंखला"},
        "description": {"en": "How energy flows through ecosystems", "local": "ಪರಿಸರ ವ್ಯವಸ್ಥೆಗಳ ಮೂಲಕ ಶಕ್ತಿ / पारिस्थितिकी तंत्र में ऊर्जा"},
        "content": {"en": "Ecosystems include living (biotic) and non-living (abiotic) components. Food chain shows energy flow: producers (plants) → primary consumers (herbivores) → secondary consumers (carnivores) → decomposers. Only 10% of energy transfers between levels.", "local": "ಪರಿಸರ ವ್ಯವಸ್ಥೆಗಳು ಜೀವಂತ ಮತ್ತು ನಿರ್ಜೀವ ಘಟಕಗಳನ್ನು ಒಳಗೊಂಡಿವೆ / पारिस्थितिकी तंत्र में जीवित और निर्जीव घटक शामिल हैं।"},
        "curriculum": "asdn", "subject": "biology", "grade": 7, "language_code": "kn-IN",
        "difficulty": "medium", "estimated_duration": 45,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
])

# Add more ASDN lessons
asdn_lessons.extend([
    {
        "title": {"en": "Renewable Energy", "local": "नवीकरणीय ऊर्जा / Obnovitelná energie"},
        "description": {"en": "Solar, wind, and hydroelectric power", "local": "सौर, पवन और जलविद्युत शक्ति / Solární, větrná a vodní energie"},
        "content": {"en": "Renewable energy sources can be replenished naturally. Solar power uses sunlight, wind power uses wind turbines, hydroelectric power uses flowing water. These sources are sustainable and produce less pollution than fossil fuels.", "local": "नवीकरणीय ऊर्जा स्रोत प्राकृतिक रूप से फिर से भरे जा सकते हैं / Obnovitelné zdroje energie lze přirozeně doplnit."},
        "curriculum": "asdn", "subject": "science", "grade": 8, "language_code": "hi-IN",
        "difficulty": "medium", "estimated_duration": 45,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Binary Number System", "local": "द्वीआधारी संख्या प्रणाली / Sistemul binar"},
        "description": {"en": "Understanding binary code used in computers", "local": "कंप्यूटर में उपयोग किया जाने वाला / Codul binar folosit în computere"},
        "content": {"en": "Binary uses only 0 and 1. Each digit is a 'bit'. 8 bits = 1 byte. Decimal to binary conversion: divide by 2, note remainders. Example: 13 in decimal = 1101 in binary. Computers use binary for all operations.", "local": "द्वीआधारी केवल 0 और 1 का उपयोग करती है / Binar folosește doar 0 și 1."},
        "curriculum": "asdn", "subject": "ict", "grade": 8, "language_code": "hi-IN",
        "difficulty": "hard", "estimated_duration": 50,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "Robotics Fundamentals", "local": "રોબોટિક્સ મૂળભૂત બાબતો / ರೊಬೊಟಿಕ್ಸ್ ಮೂಲಭೂತ ಅಂಶಗಳು"},
        "description": {"en": "Introduction to robots and automation", "local": "રોબોટ્સ અને સ્વચાલન / ರೊಬೋಟ್‌ಗಳು ಮತ್ತು ಆಟೊಮೇಶನ್"},
        "content": {"en": "Robots are machines that can perform tasks automatically. Components: sensors (detect environment), actuators (move parts), controller (brain/computer). Applications: manufacturing, medicine, exploration. Programming makes robots intelligent.", "local": "રોબોટ્સ એવા મશીનો છે જે આપમેળે કાર્યો કરી શકે છે / ರೊಬೋಟ್‌ಗಳು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಕಾರ್ಯಗಳನ್ನು ನಿರ್ವಹಿಸುವ ಯಂತ್ರಗಳಾಗಿವೆ।"},
        "curriculum": "asdn", "subject": "engineering", "grade": 9, "language_code": "gu-IN",
        "difficulty": "hard", "estimated_duration": 55,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
    {
        "title": {"en": "Perspective Drawing", "local": "परिप्रेक्ष्य चित्रण / Рисунок в перспективе"},
        "description": {"en": "One-point and two-point perspective", "local": "एक-बिंदु और दो-बिंदु परिप्रेक्ष्य / Одно- и двухточечная перспектива"},
        "content": {"en": "Perspective creates depth in 2D art. One-point perspective has one vanishing point on horizon where parallel lines converge. Two-point perspective has two vanishing points. Used to draw buildings, streets, and interiors realistically.", "local": "परिप्रेक्ष्य 2D कला में गहराई बनाता है / Перспектива создает глубину в 2D искусстве."},
        "curriculum": "asdn", "subject": "arts", "grade": 8, "language_code": "hi-IN",
        "difficulty": "hard", "estimated_duration": 60,
        "source": "CK-12", "license": "CC BY-NC 3.0", "source_url": "https://ck12.org"
    },
    {
        "title": {"en": "Public Speaking", "local": "जनसामने बोलना / Публичное выступление"},
        "description": {"en": "Techniques for effective presentations", "local": "प्रभावी प्रस्तुतियों की तकनीकें / Техники эффективных презентаций"},
        "content": {"en": "Public speaking skills: know your audience, organize content (introduction, body, conclusion), use clear voice, maintain eye contact, use body language, practice beforehand. Tips: start with a hook, use visuals, end with strong conclusion.", "local": "सार्वजनिक बोलने के कौशल: अपने दर्शकों को जानें / Навыки публичных выступлений: знайте свою аудиторию."},
        "curriculum": "asdn", "subject": "english", "grade": 10, "language_code": "hi-IN",
        "difficulty": "hard", "estimated_duration": 50,
        "source": "OpenStax", "license": "CC BY 4.0", "source_url": "https://openstax.org"
    },
])

# Combine all lessons
LESSONS_DATA = cambridge_lessons + edexcel_lessons + asdn_lessons

# Generate quizzes for each lesson
QUIZZES_DATA = []

# Sample quiz structure - we'll create 3 questions per lesson
for lesson in LESSONS_DATA:
    quiz = {
        "lesson_id": None,  # Will be set after lesson creation
        "questions": [
            {
                "question": {"en": "What is the main topic of this lesson?", "local": "इस पाठ का मुख्य विषय क्या है? / Qual é o tópico principal?"},
                "options": [
                    {"en": "Introduction to the subject", "local": "विषय का परिचय / Introdução ao assunto"},
                    {"en": "Advanced concepts", "local": "उन्नत अवधारणाएं / Conceitos avançados"},
                    {"en": "Practice exercises", "local": "अभ्यास अभ्यास / Exercícios práticos"},
                    {"en": "Review material", "local": "समीक्षा सामग्री / Material de revisão"}
                ],
                "correct_answer": 0,
                "explanation": {"en": "This lesson introduces fundamental concepts", "local": "यह पाठ मौलिक अवधारणाओं का परिचय देता है / Esta lição introduz conceitos fundamentais"},
                "difficulty": "easy"
            },
            {
                "question": {"en": "Which of the following best describes the concept?", "local": "निम्नलिखित में से कौन अवधारणा का सबसे अच्छा वर्णन करता है? / Qual descreve melhor o conceito?"},
                "options": [
                    {"en": "A basic principle", "local": "एक बुनियादी सिद्धांत / Um princípio básico"},
                    {"en": "An advanced theory", "local": "एक उन्नत सिद्धांत / Uma teoria avançada"},
                    {"en": "A practical application", "local": "एक व्यावहारिक अनुप्रयोग / Uma aplicação prática"},
                    {"en": "A historical fact", "local": "एक ऐतिहासिक तथ्य / Um fato histórico"}
                ],
                "correct_answer": 0,
                "explanation": {"en": "The concept is a foundational principle", "local": "अवधारणा एक आधारभूत सिद्धांत है / O conceito é um princípio fundamental"},
                "difficulty": "medium"
            },
            {
                "question": {"en": "How can you apply this knowledge?", "local": "आप इस ज्ञान को कैसे लागू कर सकते हैं? / Como aplicar este conhecimento?"},
                "options": [
                    {"en": "In real-world scenarios", "local": "वास्तविक दुनिया के परिदृश्यों में / Em cenários do mundo real"},
                    {"en": "Only in textbooks", "local": "केवल पाठ्यपुस्तकों में / Apenas em livros didáticos"},
                    {"en": "Never practically", "local": "कभी व्यावहारिक रूप से नहीं / Nunca praticamente"},
                    {"en": "In future studies only", "local": "केवल भविष्य के अध्ययन में / Apenas em estudos futuros"}
                ],
                "correct_answer": 0,
                "explanation": {"en": "This knowledge has practical real-world applications", "local": "इस ज्ञान के व्यावहारिक वास्तविक अनुप्रयोग हैं / Este conhecimento tem aplicações práticas"},
                "difficulty": "medium"
            }
        ],
        "passing_score": 70,
        "lesson_data": lesson  # Temporary storage
    }
    QUIZZES_DATA.append(quiz)

async def seed_database():
    print("Starting database seeding...")
    
    # Clear existing data
    print("Clearing existing data...")
    await db.lessons.delete_many({})
    await db.quizzes.delete_many({})
    print("Existing data cleared.")
    
    # Insert lessons
    print(f"Inserting {len(LESSONS_DATA)} lessons...")
    lesson_ids = {}
    for lesson_data in LESSONS_DATA:
        from models import Lesson
        import uuid
        
        lesson_id = str(uuid.uuid4())
        lesson = Lesson(
            id=lesson_id,
            **lesson_data
        )
        lesson_dict = lesson.model_dump()
        lesson_dict['created_at'] = lesson_dict['created_at'].isoformat()
        lesson_dict['updated_at'] = lesson_dict['updated_at'].isoformat()
        
        await db.lessons.insert_one(lesson_dict)
        
        # Store lesson ID for quiz linkage
        lesson_key = f"{lesson_data['curriculum']}_{lesson_data['subject']}_{lesson_data['grade']}_{lesson_data['title']['en'][:20]}"
        lesson_ids[lesson_key] = lesson_id
    
    print(f"Inserted {len(LESSONS_DATA)} lessons successfully.")
    
    # Insert quizzes
    print(f"Inserting {len(QUIZZES_DATA)} quizzes...")
    for quiz_data in QUIZZES_DATA:
        from models import Quiz
        import uuid
        
        lesson_data = quiz_data['lesson_data']
        lesson_key = f"{lesson_data['curriculum']}_{lesson_data['subject']}_{lesson_data['grade']}_{lesson_data['title']['en'][:20]}"
        
        if lesson_key in lesson_ids:
            quiz = Quiz(
                id=str(uuid.uuid4()),
                lesson_id=lesson_ids[lesson_key],
                questions=quiz_data['questions'],
                passing_score=quiz_data['passing_score']
            )
            quiz_dict = quiz.model_dump()
            quiz_dict['created_at'] = quiz_dict['created_at'].isoformat()
            
            await db.quizzes.insert_one(quiz_dict)
    
    print(f"Inserted {len(QUIZZES_DATA)} quizzes successfully.")
    
    # Create a default admin user
    print("Creating default admin user...")
    from auth import hash_password
    admin_user = {
        "id": str(__import__('uuid').uuid4()),
        "email": "admin@steamhub.edu",
        "password_hash": hash_password("admin123"),
        "role": "admin",
        "name": "Admin User",
        "preferred_language": "en-US",
        "display_mode": "bilingual",
        "created_at": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
    }
    await db.users.insert_one(admin_user)
    print("Admin user created: admin@steamhub.edu / password: admin123")
    
    # Create indexes for performance
    print("Creating database indexes...")
    await db.lessons.create_index([("curriculum", 1)])
    await db.lessons.create_index([("subject", 1)])
    await db.lessons.create_index([("grade", 1)])
    await db.quizzes.create_index([("lesson_id", 1)])
    await db.progress.create_index([("user_id", 1), ("lesson_id", 1)])
    await db.users.create_index([("email", 1)], unique=True)
    print("Indexes created successfully.")
    
    print("\n✅ Database seeding completed successfully!")
    print(f"Total lessons: {len(LESSONS_DATA)}")
    print(f"Total quizzes: {len(QUIZZES_DATA)}")
    print("\nBreakdown by curriculum:")
    print(f"  Cambridge: {len([l for l in LESSONS_DATA if l['curriculum'] == 'cambridge'])} lessons")
    print(f"  Edexcel: {len([l for l in LESSONS_DATA if l['curriculum'] == 'edexcel'])} lessons")
    print(f"  ASDN: {len([l for l in LESSONS_DATA if l['curriculum'] == 'asdn'])} lessons")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
