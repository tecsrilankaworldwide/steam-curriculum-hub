import React, { useState, useMemo } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Search, BookOpen, Globe, Volume2 } from 'lucide-react';
import { useLanguage } from '../App';
import { speak } from '../utils/tts';

// Comprehensive AI/STEAM glossary with translations
const GLOSSARY_TERMS = [
  {
    term: "Artificial Intelligence (AI)",
    definition: "A field of computer science that creates systems capable of performing tasks that normally require human intelligence.",
    category: "Core AI",
    translations: {
      si: { term: "කෘත්‍රිම බුද්ධිය (AI)", definition: "මිනිස් බුද්ධිය සාමාන්‍යයෙන් අවශ්‍ය වන කාර්යයන් සිදු කිරීමට හැකි පද්ධති නිර්මාණය කරන පරිගණක විද්‍යාවේ ක්ෂේත්‍රයකි." },
      ta: { term: "செயற்கை நுண்ணறிவு (AI)", definition: "மனித நுண்ணறிவு பொதுவாகத் தேவைப்படும் பணிகளைச் செய்யக்கூடிய அமைப்புகளை உருவாக்கும் கணினி அறிவியல் துறை." }
    }
  },
  {
    term: "Machine Learning (ML)",
    definition: "A subset of AI where computers learn from data and improve their performance without being explicitly programmed.",
    category: "Core AI",
    translations: {
      si: { term: "යන්ත්‍ර ඉගෙනීම (ML)", definition: "පරිගණක දත්ත වලින් ඉගෙනගෙන පැහැදිලිව ක්‍රමලේඛනය නොකර ඔවුන්ගේ කාර්ය සාධනය වැඩිදියුණු කරන AI හි උප කුලකයකි." },
      ta: { term: "இயந்திர கற்றல் (ML)", definition: "கணினிகள் தரவுகளிலிருந்து கற்றுக்கொண்டு, வெளிப்படையாக நிரலாக்கப்படாமல் தங்கள் செயல்திறனை மேம்படுத்தும் AI-யின் துணைக்குழு." }
    }
  },
  {
    term: "Neural Network",
    definition: "A computing system inspired by the human brain, made up of interconnected nodes (neurons) that process information.",
    category: "Core AI",
    translations: {
      si: { term: "ස්නායු ජාලය", definition: "මිනිස් මොළයෙන් ආභාසය ලබූ, තොරතුරු සකසන අන්තර් සම්බන්ධිත නෝඩ් (නියුරෝන) වලින් සමන්විත පරිගණක පද්ධතියකි." },
      ta: { term: "நரம்பு வலையமைப்பு", definition: "மனித மூளையால் ஊக்கமளிக்கப்பட்ட, தகவலை செயலாக்கும் ஒன்றோடொன்று இணைக்கப்பட்ட முனைகளால் (நியூரான்கள்) ஆன கணினி அமைப்பு." }
    }
  },
  {
    term: "Deep Learning",
    definition: "A type of machine learning using multiple layers of neural networks to analyze complex patterns in data.",
    category: "Core AI",
    translations: {
      si: { term: "ගැඹුරු ඉගෙනීම", definition: "දත්තවල සංකීර්ණ රටා විශ්ලේෂණය කිරීමට ස්නායු ජාල වල බහු ස්ථර භාවිතා කරන යන්ත්‍ර ඉගෙනීමේ වර්ගයකි." },
      ta: { term: "ஆழ்ந்த கற்றல்", definition: "தரவுகளில் சிக்கலான வடிவங்களை பகுப்பாய்வு செய்ய நரம்பு வலையமைப்புகளின் பல அடுக்குகளைப் பயன்படுத்தும் இயந்திர கற்றல் வகை." }
    }
  },
  {
    term: "Algorithm",
    definition: "A step-by-step set of instructions or rules that a computer follows to solve a problem or complete a task.",
    category: "Programming",
    translations: {
      si: { term: "ඇල්ගොරිතම", definition: "ගැටලුවක් විසඳීමට හෝ කාර්යයක් සම්පූර්ණ කිරීමට පරිගණකයක් අනුගමනය කරන පියවරෙන් පියවර උපදෙස් හෝ නීති සමූහයකි." },
      ta: { term: "வழிமுறை", definition: "ஒரு சிக்கலைத் தீர்க்க அல்லது ஒரு பணியை முடிக்க கணினி பின்பற்றும் படிப்படியான வழிமுறைகள் அல்லது விதிகளின் தொகுப்பு." }
    }
  },
  {
    term: "Data",
    definition: "Raw facts, numbers, text, or images that computers collect, store, and process to find useful information.",
    category: "Data Science",
    translations: {
      si: { term: "දත්ත", definition: "ප්‍රයෝජනවත් තොරතුරු සොයා ගැනීමට පරිගණක එකතු කරන, ගබඩා කරන සහ සකසන අමු කරුණු, අංක, පෙළ හෝ රූප." },
      ta: { term: "தரவு", definition: "பயனுள்ள தகவல்களைக் கண்டறிய கணினிகள் சேகரிக்கும், சேமிக்கும் மற்றும் செயலாக்கும் மூல உண்மைகள், எண்கள், உரை அல்லது படங்கள்." }
    }
  },
  {
    term: "Robot",
    definition: "A machine that can be programmed to carry out tasks automatically, often using sensors and AI to interact with its environment.",
    category: "Robotics",
    translations: {
      si: { term: "රොබෝ", definition: "එහි පරිසරය සමඟ අන්තර්ක්‍රියා කිරීමට බොහෝ විට සංවේදක සහ AI භාවිතා කරමින්, ස්වයංක්‍රීයව කාර්යයන් සිදු කිරීමට ක්‍රමලේඛනය කළ හැකි යන්ත්‍රයකි." },
      ta: { term: "ரோபோ", definition: "தன் சூழலுடன் தொடர்புகொள்ள பெரும்பாலும் சென்சார்கள் மற்றும் AI-ஐப் பயன்படுத்தி, தானாகவே பணிகளைச் செய்ய நிரலாக்கக்கூடிய இயந்திரம்." }
    }
  },
  {
    term: "Natural Language Processing (NLP)",
    definition: "The ability of computers to understand, interpret, and generate human language like English, Sinhala, or Tamil.",
    category: "Core AI",
    translations: {
      si: { term: "ස්වාභාවික භාෂා සැකසීම (NLP)", definition: "ඉංග්‍රීසි, සිංහල හෝ දෙමළ වැනි මිනිස් භාෂාව තේරුම් ගැනීමට, අර්ථ නිරූපණය කිරීමට සහ ජනනය කිරීමට පරිගණකවලට ඇති හැකියාවයි." },
      ta: { term: "இயற்கை மொழி செயலாக்கம் (NLP)", definition: "ஆங்கிலம், சிங்களம் அல்லது தமிழ் போன்ற மனித மொழியைப் புரிந்துகொள்ளவும், விளக்கவும், உருவாக்கவும் கணினிகளின் திறன்." }
    }
  },
  {
    term: "Computer Vision",
    definition: "AI technology that enables computers to 'see' and understand images and videos, like recognizing faces or objects.",
    category: "Core AI",
    translations: {
      si: { term: "පරිගණක දෘෂ්ටිය", definition: "මුහුණු හෝ වස්තු හඳුනා ගැනීම වැනි, රූප සහ වීඩියෝ 'බැලීමට' සහ තේරුම් ගැනීමට පරිගණකවලට හැකි AI තාක්ෂණය." },
      ta: { term: "கணினி பார்வை", definition: "முகங்கள் அல்லது பொருட்களை அடையாளம் காண்பது போன்ற, படங்கள் மற்றும் வீடியோக்களை 'பார்க்கவும்' புரிந்துகொள்ளவும் கணினிகளுக்கு உதவும் AI தொழில்நுட்பம்." }
    }
  },
  {
    term: "Chatbot",
    definition: "A computer program that can have conversations with humans using text or voice, like a virtual assistant.",
    category: "Applications",
    translations: {
      si: { term: "චැට්බොට්", definition: "අතථ්‍ය සහායකයෙකු වැනි, පෙළ හෝ හඬ භාවිතයෙන් මිනිසුන් සමඟ සංවාද කළ හැකි පරිගණක වැඩසටහනකි." },
      ta: { term: "சாட்போட்", definition: "மெய்நிகர் உதவியாளர் போன்ற, உரை அல்லது குரலைப் பயன்படுத்தி மனிதர்களுடன் உரையாடக்கூடிய கணினி நிரல்." }
    }
  },
  {
    term: "Training Data",
    definition: "The collection of examples used to teach an AI system how to make predictions or decisions.",
    category: "Data Science",
    translations: {
      si: { term: "පුහුණු දත්ත", definition: "පුරෝකථන හෝ තීරණ ගන්නේ කෙසේදැයි AI පද්ධතියකට ඉගැන්වීමට භාවිතා කරන උදාහරණ එකතුව." },
      ta: { term: "பயிற்சி தரவு", definition: "ஒரு AI அமைப்புக்கு கணிப்புகள் அல்லது முடிவுகளை எடுப்பது எப்படி என்று கற்பிக்கப் பயன்படுத்தப்படும் எடுத்துக்காட்டுகளின் தொகுப்பு." }
    }
  },
  {
    term: "Supervised Learning",
    definition: "A type of machine learning where the computer learns from labeled examples with correct answers provided.",
    category: "Core AI",
    translations: {
      si: { term: "අධීක්ෂිත ඉගෙනීම", definition: "නිවැරදි පිළිතුරු සපයා ඇති ලේබල් කළ උදාහරණ වලින් පරිගණකය ඉගෙන ගන්නා යන්ත්‍ර ඉගෙනීමේ වර්ගයකි." },
      ta: { term: "மேற்பார்வையிடப்பட்ட கற்றல்", definition: "சரியான பதில்கள் வழங்கப்பட்ட லேபிளிடப்பட்ட எடுத்துக்காட்டுகளிலிருந்து கணினி கற்றுக்கொள்ளும் இயந்திர கற்றல் வகை." }
    }
  },
  {
    term: "Coding / Programming",
    definition: "Writing instructions in a special language that computers can understand and follow to perform tasks.",
    category: "Programming",
    translations: {
      si: { term: "කේතකරණය / ක්‍රමලේඛනය", definition: "කාර්යයන් සිදු කිරීමට පරිගණකවලට තේරුම් ගත හැකි සහ අනුගමනය කළ හැකි විශේෂ භාෂාවකින් උපදෙස් ලිවීම." },
      ta: { term: "குறியீட்டு / நிரலாக்கம்", definition: "பணிகளைச் செய்ய கணினிகள் புரிந்துகொள்ளக்கூடிய மற்றும் பின்பற்றக்கூடிய சிறப்பு மொழியில் வழிமுறைகளை எழுதுதல்." }
    }
  },
  {
    term: "Sensor",
    definition: "A device that detects changes in the environment (like light, sound, temperature) and sends this information to a computer.",
    category: "Robotics",
    translations: {
      si: { term: "සංවේදකය", definition: "පරිසරයේ වෙනස්කම් (ආලෝකය, ශබ්දය, උෂ්ණත්වය වැනි) හඳුනාගෙන මෙම තොරතුරු පරිගණකයකට යවන උපකරණයකි." },
      ta: { term: "சென்சார்", definition: "சுற்றுச்சூழலில் மாற்றங்களை (ஒளி, ஒலி, வெப்பநிலை போன்றவை) கண்டறிந்து இந்த தகவலை கணினிக்கு அனுப்பும் சாதனம்." }
    }
  },
  {
    term: "Ethics in AI",
    definition: "The study of right and wrong in how AI is created and used, ensuring it is fair, safe, and respects privacy.",
    category: "Ethics",
    translations: {
      si: { term: "AI හි ආචාරධර්ම", definition: "AI නිර්මාණය කරන සහ භාවිතා කරන ආකාරය පිළිබඳ නිවැරදි සහ වැරදි අධ්‍යයනය, එය සාධාරණ, ආරක්ෂිත සහ පෞද්ගලිකත්වයට ගරු කරන බව සහතික කිරීම." },
      ta: { term: "AI-யில் நெறிமுறைகள்", definition: "AI உருவாக்கப்படும் மற்றும் பயன்படுத்தப்படும் விதத்தில் சரி மற்றும் தவறை ஆய்வு செய்தல், அது நியாயமானது, பாதுகாப்பானது மற்றும் தனியுரிமையை மதிக்கிறது என்பதை உறுதி செய்தல்." }
    }
  },
  {
    term: "Bias in AI",
    definition: "When an AI system makes unfair decisions because the data it learned from was not balanced or representative.",
    category: "Ethics",
    translations: {
      si: { term: "AI හි පක්ෂපාතිත්වය", definition: "AI පද්ධතියක් අසාධාරණ තීරණ ගන්නේ එය ඉගෙන ගත් දත්ත සමතුලිත හෝ නියෝජිත නොවූ නිසාය." },
      ta: { term: "AI-யில் சார்பு", definition: "AI அமைப்பு நியாயமற்ற முடிவுகளை எடுப்பது, ஏனெனில் அது கற்றுக்கொண்ட தரவு சமநிலையாக அல்லது பிரதிநிதித்துவமாக இல்லை." }
    }
  },
  {
    term: "Internet of Things (IoT)",
    definition: "A network of everyday objects (like smart watches, home appliances) connected to the internet, sharing data with each other.",
    category: "Technology",
    translations: {
      si: { term: "අන්තර්ජාල වස්තු (IoT)", definition: "අන්තර්ජාලයට සම්බන්ධ, එකිනෙකා සමඟ දත්ත බෙදා ගන්නා දෛනික වස්තු (ස්මාර්ට් ඔරලෝසු, ගෘහ උපකරණ වැනි) ජාලයකි." },
      ta: { term: "இணையத்தின் பொருட்கள் (IoT)", definition: "இணையத்துடன் இணைக்கப்பட்ட, ஒருவருக்கொருவர் தரவைப் பகிர்ந்துகொள்ளும் அன்றாடப் பொருட்களின் (ஸ்மார்ட் வாட்ச்கள், வீட்டு உபகரணங்கள் போன்றவை) நெட்வொர்க்." }
    }
  },
  {
    term: "Cloud Computing",
    definition: "Using remote servers on the internet to store, manage, and process data instead of a local computer.",
    category: "Technology",
    translations: {
      si: { term: "වලාකුළු පරිගණනය", definition: "දේශීය පරිගණකයක් වෙනුවට දත්ත ගබඩා කිරීමට, කළමනාකරණය කිරීමට සහ සැකසීමට අන්තර්ජාලයේ දුරස්ථ සේවාදායක භාවිතා කිරීම." },
      ta: { term: "கிளவுட் கம்ப்யூட்டிங்", definition: "உள்ளூர் கணினிக்கு பதிலாக தரவை சேமிக்க, நிர்வகிக்க மற்றும் செயலாக்க இணையத்தில் உள்ள தொலைநிலை சர்வர்களைப் பயன்படுத்துதல்." }
    }
  },
  {
    term: "3D Printing",
    definition: "Creating three-dimensional objects by building them layer by layer from digital designs using special printers.",
    category: "STEAM",
    translations: {
      si: { term: "3D මුද්‍රණය", definition: "විශේෂ මුද්‍රණ යන්ත්‍ර භාවිතා කරමින් ඩිජිටල් සැලසුම් වලින් ස්ථරයෙන් ස්ථරයක් ගොඩනඟමින් ත්‍රිමාණ වස්තු නිර්මාණය කිරීම." },
      ta: { term: "3D அச்சிடுதல்", definition: "சிறப்பு அச்சுப்பொறிகளைப் பயன்படுத்தி டிஜிட்டல் வடிவமைப்புகளிலிருந்து அடுக்கு அடுக்காக கட்டமைத்து முப்பரிமாண பொருட்களை உருவாக்குதல்." }
    }
  },
  {
    term: "Virtual Reality (VR)",
    definition: "Technology that creates a completely simulated environment you can explore using special headsets and controllers.",
    category: "Technology",
    translations: {
      si: { term: "අතථ්‍ය යථාර්ථය (VR)", definition: "විශේෂ හෙඩ්සෙට් සහ පාලක භාවිතා කරමින් ඔබට ගවේෂණය කළ හැකි සම්පූර්ණයෙන් අනුකරණය කළ පරිසරයක් නිර්මාණය කරන තාක්ෂණය." },
      ta: { term: "மெய்நிகர் யதார்த்தம் (VR)", definition: "சிறப்பு ஹெட்செட்கள் மற்றும் கன்ட்ரோலர்களைப் பயன்படுத்தி நீங்கள் ஆராயக்கூடிய முழுமையாக உருவகப்படுத்தப்பட்ட சூழலை உருவாக்கும் தொழில்நுட்பம்." }
    }
  },
  {
    term: "Reinforcement Learning",
    definition: "A type of machine learning where an AI agent learns by trying different actions and receiving rewards or penalties.",
    category: "Core AI",
    translations: {
      si: { term: "ශක්තිමත් ඉගෙනීම", definition: "AI නියෝජිතයෙකු විවිධ ක්‍රියා උත්සාහ කිරීමෙන් සහ ත්‍යාග හෝ දඩ ලැබීමෙන් ඉගෙන ගන්නා යන්ත්‍ර ඉගෙනීමේ වර්ගයකි." },
      ta: { term: "வலுவூட்டல் கற்றல்", definition: "AI முகவர் வெவ்வேறு செயல்களை முயற்சிப்பதன் மூலமும் வெகுமதிகள் அல்லது அபராதங்களைப் பெறுவதன் மூலமும் கற்றுக்கொள்ளும் இயந்திர கற்றல் வகை." }
    }
  },
  {
    term: "Autonomous Vehicle",
    definition: "A car or vehicle that can drive itself without a human driver, using sensors, cameras, and AI to navigate roads safely.",
    category: "Applications",
    translations: {
      si: { term: "ස්වයංක්‍රීය වාහනය", definition: "මාර්ග ආරක්ෂිතව සැරිසැරීමට සංවේදක, කැමරා සහ AI භාවිතා කරමින්, මිනිස් රියදුරුවකු නොමැතිව තනිවම ධාවනය කළ හැකි මෝටර් රථයක් හෝ වාහනයකි." },
      ta: { term: "தன்னியக்க வாகனம்", definition: "சாலைகளில் பாதுகாப்பாகச் செல்ல சென்சார்கள், கேமராக்கள் மற்றும் AI-ஐப் பயன்படுத்தி, மனித ஓட்டுநர் இல்லாமல் தானாக ஓட்டக்கூடிய கார் அல்லது வாகனம்." }
    }
  },
  {
    term: "Augmented Reality (AR)",
    definition: "Technology that adds digital images or information on top of what you see in the real world through a phone or glasses.",
    category: "Technology",
    translations: {
      si: { term: "වැඩිදියුණු කළ යථාර්ථය (AR)", definition: "දුරකථනයක් හෝ කණ්ණාඩි හරහා සැබෑ ලෝකයේ ඔබ දකින දේට ඉහළින් ඩිජිටල් රූප හෝ තොරතුරු එකතු කරන තාක්ෂණය." },
      ta: { term: "மெருகூட்டப்பட்ட யதார்த்தம் (AR)", definition: "தொலைபேசி அல்லது கண்ணாடி வழியாக நீங்கள் நிஜ உலகில் பார்ப்பவற்றின் மேல் டிஜிட்டல் படங்கள் அல்லது தகவல்களைச் சேர்க்கும் தொழில்நுட்பம்." }
    }
  },
  {
    term: "Generative AI",
    definition: "AI systems that can create new content like text, images, music, or videos based on patterns learned from existing data.",
    category: "Core AI",
    translations: {
      si: { term: "ජනක AI", definition: "පවතින දත්ත වලින් ඉගෙන ගත් රටා මත පදනම්ව පෙළ, රූප, සංගීතය හෝ වීඩියෝ වැනි නව අන්තර්ගතයන් නිර්මාණය කළ හැකි AI පද්ධති." },
      ta: { term: "உருவாக்கும் AI", definition: "ஏற்கனவே உள்ள தரவுகளிலிருந்து கற்றுக்கொண்ட வடிவங்களின் அடிப்படையில் உரை, படங்கள், இசை அல்லது வீடியோக்கள் போன்ற புதிய உள்ளடக்கத்தை உருவாக்கக்கூடிய AI அமைப்புகள்." }
    }
  },
  {
    term: "Prompt Engineering",
    definition: "The skill of writing clear and effective instructions (prompts) to get the best results from AI systems like ChatGPT.",
    category: "Applications",
    translations: {
      si: { term: "ප්‍රොම්ප්ට් ඉංජිනේරු විද්‍යාව", definition: "ChatGPT වැනි AI පද්ධති වලින් හොඳම ප්‍රතිඵල ලබා ගැනීමට පැහැදිලි සහ ඵලදායී උපදෙස් (ප්‍රොම්ප්ට්) ලිවීමේ කුසලතාව." },
      ta: { term: "ப்ராம்ப்ட் பொறியியல்", definition: "ChatGPT போன்ற AI அமைப்புகளிலிருந்து சிறந்த முடிவுகளைப் பெற தெளிவான மற்றும் பயனுள்ள வழிமுறைகளை (ப்ராம்ப்ட்) எழுதும் திறன்." }
    }
  },
  {
    term: "Binary Code",
    definition: "The language of computers using only two digits: 0 and 1. All information in a computer is stored and processed as binary.",
    category: "Programming",
    translations: {
      si: { term: "ද්විමය කේතය", definition: "අංක දෙකක් පමණක් භාවිතා කරන පරිගණකවල භාෂාව: 0 සහ 1. පරිගණකයක සියලුම තොරතුරු ද්විමය ලෙස ගබඩා කර සකසනු ලැබේ." },
      ta: { term: "இருமக் குறியீடு", definition: "இரண்டு இலக்கங்களை மட்டும் பயன்படுத்தும் கணினிகளின் மொழி: 0 மற்றும் 1. கணினியில் உள்ள அனைத்து தகவல்களும் இருமத்தில் சேமிக்கப்பட்டு செயலாக்கப்படுகின்றன." }
    }
  },
  {
    term: "Pixel",
    definition: "The smallest single point of color in a digital image. Millions of pixels together form the pictures you see on screens.",
    category: "STEAM",
    translations: {
      si: { term: "පික්සලය", definition: "ඩිජිටල් රූපයක කුඩාම තනි වර්ණ ලක්ෂ්‍යය. පික්සල මිලියන ගණනක් එකට තිර මත ඔබ දකින චිත්‍ර සාදයි." },
      ta: { term: "பிக்சல்", definition: "டிஜிட்டல் படத்தில் மிகச்சிறிய ஒற்றை நிற புள்ளி. மில்லியன் கணக்கான பிக்சல்கள் ஒன்றாக திரைகளில் நீங்கள் பார்க்கும் படங்களை உருவாக்குகின்றன." }
    }
  },
  {
    term: "Cybersecurity",
    definition: "The practice of protecting computers, networks, and data from unauthorized access, attacks, and damage.",
    category: "Technology",
    translations: {
      si: { term: "සයිබර් ආරක්ෂාව", definition: "අනවසර ප්‍රවේශය, ප්‍රහාර සහ හානි වලින් පරිගණක, ජාල සහ දත්ත ආරක්ෂා කිරීමේ පුහුණුව." },
      ta: { term: "சைபர் பாதுகாப்பு", definition: "அங்கீகரிக்கப்படாத அணுகல், தாக்குதல்கள் மற்றும் சேதத்திலிருந்து கணினிகள், நெட்வொர்க்குகள் மற்றும் தரவைப் பாதுகாக்கும் நடைமுறை." }
    }
  },
  {
    term: "API (Application Programming Interface)",
    definition: "A set of rules that allows different software programs to communicate with each other and share data.",
    category: "Programming",
    translations: {
      si: { term: "API (යෙදුම් ක්‍රමලේඛන අතුරුමුහුණත)", definition: "විවිධ මෘදුකාංග වැඩසටහන් එකිනෙකා සමඟ සන්නිවේදනය කිරීමට සහ දත්ත බෙදා ගැනීමට ඉඩ සලසන නීති සමූහයකි." },
      ta: { term: "API (பயன்பாட்டு நிரலாக்க இடைமுகம்)", definition: "வெவ்வேறு மென்பொருள் நிரல்கள் ஒருவருக்கொருவர் தொடர்புகொள்ளவும் தரவைப் பகிர்ந்துகொள்ளவும் அனுமதிக்கும் விதிகளின் தொகுப்பு." }
    }
  },
  {
    term: "Big Data",
    definition: "Extremely large collections of data that are too complex for traditional methods to process, requiring special tools and AI.",
    category: "Data Science",
    translations: {
      si: { term: "විශාල දත්ත", definition: "සාම්ප්‍රදායික ක්‍රම මගින් සැකසීමට තරම් සංකීර්ණ, විශේෂ මෙවලම් සහ AI අවශ්‍ය වන අතිශයින් විශාල දත්ත එකතුවක්." },
      ta: { term: "பெரிய தரவு", definition: "பாரம்பரிய முறைகளால் செயலாக்க முடியாத அளவு சிக்கலான, சிறப்பு கருவிகள் மற்றும் AI தேவைப்படும் மிகப்பெரிய தரவு தொகுப்புகள்." }
    }
  },
  {
    term: "Machine Translation",
    definition: "Using AI to automatically translate text from one language to another, like translating English to Sinhala.",
    category: "Applications",
    translations: {
      si: { term: "යන්ත්‍ර පරිවර්තනය", definition: "ඉංග්‍රීසි සිට සිංහලට පරිවර්තනය කිරීම වැනි, එක් භාෂාවකින් තවත් භාෂාවකට ස්වයංක්‍රීයව පරිවර්තනය කිරීමට AI භාවිතා කිරීම." },
      ta: { term: "இயந்திர மொழிபெயர்ப்பு", definition: "ஆங்கிலத்தை சிங்களத்திற்கு மொழிபெயர்ப்பது போன்ற, ஒரு மொழியிலிருந்து மற்றொரு மொழிக்கு உரையை தானாக மொழிபெயர்க்க AI-ஐப் பயன்படுத்துதல்." }
    }
  },
  {
    term: "Blockchain",
    definition: "A secure digital record-keeping system where data is stored in linked blocks, making it very hard to change or cheat.",
    category: "Technology",
    translations: {
      si: { term: "බ්ලොක්චේන්", definition: "දත්ත සම්බන්ධිත කොටස් වල ගබඩා කර ඇති ආරක්ෂිත ඩිජිටල් වාර්තා තබා ගැනීමේ පද්ධතියක් වන අතර එය වෙනස් කිරීම හෝ වංචා කිරීම ඉතා දුෂ්කර ය." },
      ta: { term: "பிளாக்செயின்", definition: "இணைக்கப்பட்ட தொகுதிகளில் தரவு சேமிக்கப்பட்டு, மாற்றுவது அல்லது ஏமாற்றுவது மிகவும் கடினமான பாதுகாப்பான டிஜிட்டல் பதிவு வைப்பு அமைப்பு." }
    }
  },
  {
    term: "Image Recognition",
    definition: "AI's ability to identify objects, people, places, or actions in photographs and videos.",
    category: "Core AI",
    translations: {
      si: { term: "රූප හඳුනාගැනීම", definition: "ඡායාරූප සහ වීඩියෝ වල වස්තු, පුද්ගලයන්, ස්ථාන හෝ ක්‍රියා හඳුනා ගැනීමට AI ට ඇති හැකියාව." },
      ta: { term: "பட அங்கீகாரம்", definition: "புகைப்படங்கள் மற்றும் வீடியோக்களில் பொருட்கள், நபர்கள், இடங்கள் அல்லது செயல்களை அடையாளம் காணும் AI-யின் திறன்." }
    }
  },
  {
    term: "Smart Home",
    definition: "A house equipped with internet-connected devices that can be controlled automatically or remotely, like smart lights and thermostats.",
    category: "Applications",
    translations: {
      si: { term: "ස්මාර්ට් නිවස", definition: "ස්මාර්ට් ලයිට් සහ තාපස්ථායක වැනි, ස්වයංක්‍රීයව හෝ දුරස්ථව පාලනය කළ හැකි අන්තර්ජාලයට සම්බන්ධ උපාංග සහිත නිවසක්." },
      ta: { term: "ஸ்மார்ட் வீடு", definition: "ஸ்மார்ட் விளக்குகள் மற்றும் தெர்மோஸ்டாட்கள் போன்ற, தானாக அல்லது தொலைநிலையில் கட்டுப்படுத்தக்கூடிய இணையத்துடன் இணைக்கப்பட்ட சாதனங்கள் பொருத்தப்பட்ட வீடு." }
    }
  },
  {
    term: "Neural Language Model",
    definition: "An AI system trained on huge amounts of text to understand and generate human-like language, like GPT or BERT.",
    category: "Core AI",
    translations: {
      si: { term: "ස්නායු භාෂා ආකෘතිය", definition: "GPT හෝ BERT වැනි, මිනිස් වැනි භාෂාව තේරුම් ගැනීමට සහ ජනනය කිරීමට විශාල පෙළ ප්‍රමාණයක් මත පුහුණු කරන ලද AI පද්ධතියකි." },
      ta: { term: "நரம்பு மொழி மாதிரி", definition: "GPT அல்லது BERT போன்ற, மனிதனைப் போன்ற மொழியைப் புரிந்துகொள்ளவும் உருவாக்கவும் பெரிய அளவிலான உரையில் பயிற்சி பெற்ற AI அமைப்பு." }
    }
  },
  {
    term: "Debugging",
    definition: "The process of finding and fixing errors (bugs) in computer programs to make them work correctly.",
    category: "Programming",
    translations: {
      si: { term: "දෝෂ නිරාකරණය", definition: "පරිගණක වැඩසටහන් නිවැරදිව ක්‍රියා කරවීමට ඒවායේ දෝෂ (bugs) සොයා ගැනීමේ සහ නිවැරදි කිරීමේ ක්‍රියාවලිය." },
      ta: { term: "பிழைத்திருத்தம்", definition: "கணினி நிரல்களில் உள்ள பிழைகளை (bugs) கண்டறிந்து சரிசெய்து அவை சரியாக வேலை செய்யும்படி செய்யும் செயல்முறை." }
    }
  },
  {
    term: "Simulation",
    definition: "A computer model that imitates a real-world process or system, used for testing, training, or understanding.",
    category: "STEAM",
    translations: {
      si: { term: "අනුකරණය", definition: "පරීක්ෂණ, පුහුණුව හෝ අවබෝධය සඳහා භාවිතා කරන, සැබෑ ලෝක ක්‍රියාවලියක් හෝ පද්ධතියක් අනුකරණය කරන පරිගණක ආකෘතියකි." },
      ta: { term: "உருவகப்படுத்துதல்", definition: "சோதனை, பயிற்சி அல்லது புரிந்துகொள்ளுதலுக்கு பயன்படுத்தப்படும், நிஜ உலக செயல்முறை அல்லது அமைப்பை பின்பற்றும் கணினி மாதிரி." }
    }
  },
  {
    term: "Drone",
    definition: "An unmanned flying vehicle controlled remotely or by AI, used for photography, delivery, agriculture, and more.",
    category: "Robotics",
    translations: {
      si: { term: "ඩ්‍රෝනය", definition: "ඡායාරූපකරණය, බෙදාහැරීම, කෘෂිකර්මය සහ තවත් දේ සඳහා භාවිතා කරන, දුරස්ථව හෝ AI මගින් පාලනය කරන මිනිසුන් නොමැති පියාසර වාහනයකි." },
      ta: { term: "ட்ரோன்", definition: "புகைப்படம் எடுத்தல், டெலிவரி, விவசாயம் மற்றும் பலவற்றிற்கு பயன்படுத்தப்படும், தொலைநிலையில் அல்லது AI மூலம் கட்டுப்படுத்தப்படும் ஆளில்லா பறக்கும் வாகனம்." }
    }
  },
  {
    term: "Facial Recognition",
    definition: "AI technology that can identify a person by analyzing the unique features of their face from photos or video.",
    category: "Applications",
    translations: {
      si: { term: "මුහුණු හඳුනාගැනීම", definition: "ඡායාරූප හෝ වීඩියෝ වලින් පුද්ගලයෙකුගේ මුහුණේ අද්විතීය ලක්ෂණ විශ්ලේෂණය කිරීමෙන් පුද්ගලයෙකු හඳුනාගත හැකි AI තාක්ෂණය." },
      ta: { term: "முக அங்கீகாரம்", definition: "புகைப்படங்கள் அல்லது வீடியோவிலிருந்து ஒருவரின் முகத்தின் தனித்துவமான அம்சங்களை பகுப்பாய்வு செய்வதன் மூலம் ஒரு நபரை அடையாளம் காணக்கூடிய AI தொழில்நுட்பம்." }
    }
  },
];

const CATEGORIES = [...new Set(GLOSSARY_TERMS.map(t => t.category))];

const LANGUAGE_NAMES = {
  en: 'English',
  si: 'සිංහල (Sinhala)',
  ta: 'தமிழ் (Tamil)',
};

const GlossaryPage = () => {
  const { language } = useLanguage();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedLang, setSelectedLang] = useState('');

  // Map frontend lang code to DB code
  const dbLang = useMemo(() => {
    const map = { 'en-US': 'en', 'si-LK': 'si', 'ta-IN': 'ta', 'hi-IN': 'hi', 'zh-CN': 'zh' };
    return map[language] || 'en';
  }, [language]);

  // Auto-select native language based on current language
  const activeLang = selectedLang || (dbLang !== 'en' ? dbLang : 'si');

  const filteredTerms = useMemo(() => {
    let terms = GLOSSARY_TERMS;
    
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      terms = terms.filter(t => 
        t.term.toLowerCase().includes(q) || 
        t.definition.toLowerCase().includes(q) ||
        (t.translations[activeLang]?.term || '').toLowerCase().includes(q)
      );
    }
    
    if (selectedCategory) {
      terms = terms.filter(t => t.category === selectedCategory);
    }
    
    return terms;
  }, [searchQuery, selectedCategory, activeLang]);

  return (
    <div className="min-h-screen bg-background py-8 px-4" data-testid="glossary-page">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-semibold tracking-tight mb-2 flex items-center gap-3" data-testid="glossary-title">
            <BookOpen className="w-9 h-9 text-primary" />
            AI & STEAM Word Glossary
          </h1>
          <p className="text-lg text-muted-foreground">
            Learn key AI and technology terms in English and your native language
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3 mb-6">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search terms..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
              data-testid="glossary-search"
            />
          </div>
          
          <select
            className="border rounded px-3 py-2 bg-background"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            data-testid="glossary-category-filter"
          >
            <option value="">All Categories</option>
            {CATEGORIES.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>

          <select
            className="border rounded px-3 py-2 bg-background"
            value={activeLang}
            onChange={(e) => setSelectedLang(e.target.value)}
            data-testid="glossary-lang-filter"
          >
            {Object.entries(LANGUAGE_NAMES).filter(([k]) => k !== 'en').map(([code, name]) => (
              <option key={code} value={code}>{name}</option>
            ))}
          </select>
        </div>

        {/* Stats */}
        <div className="flex gap-2 mb-6 flex-wrap">
          <Badge variant="outline">{filteredTerms.length} terms</Badge>
          <Badge variant="outline" className="text-primary border-primary">
            <Globe className="w-3 h-3 mr-1" />
            {LANGUAGE_NAMES[activeLang]}
          </Badge>
        </div>

        {/* Glossary Grid */}
        <div className="space-y-4">
          {filteredTerms.map((item, idx) => {
            const translation = item.translations[activeLang];
            return (
              <Card key={idx} className="transition-all duration-200 hover:shadow-md" data-testid={`glossary-term-${idx}`}>
                <CardContent className="pt-5 pb-5">
                  <div className="grid md:grid-cols-2 gap-6">
                    {/* English */}
                    <div>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <h3 className="text-lg font-bold text-primary">{item.term}</h3>
                        <Badge variant="secondary" className="text-xs whitespace-nowrap">{item.category}</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground leading-relaxed">{item.definition}</p>
                    </div>

                    {/* Translation */}
                    <div className="md:border-l md:pl-6">
                      {translation ? (
                        <>
                          <div className="flex items-start justify-between gap-2 mb-2">
                            <h3 className="text-lg font-bold">{translation.term}</h3>
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-7 w-7 p-0"
                              onClick={() => speak(translation.term, language)}
                              data-testid={`glossary-speak-${idx}`}
                            >
                              <Volume2 className="w-4 h-4" />
                            </Button>
                          </div>
                          <p className="text-sm leading-relaxed">{translation.definition}</p>
                        </>
                      ) : (
                        <p className="text-sm text-muted-foreground italic">Translation coming soon...</p>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {filteredTerms.length === 0 && (
          <div className="text-center py-16">
            <BookOpen className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-lg text-muted-foreground">No terms found matching your search.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default GlossaryPage;
