import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useTranslation } from 'react-i18next';
import { Volume2 } from 'lucide-react';
import './i18n';
import api from './api';
import { speak, LANGUAGES } from './utils/tts';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './components/ui/card';
import { Badge } from './components/ui/badge';
import { Toaster, toast } from './components/ui/sonner';
import LessonDetail from './pages/LessonDetail';
import AdminDashboard from './pages/AdminDashboard';
import InquiryForm from './pages/InquiryForm';
import AcademicCalendar from './pages/AcademicCalendar';
import PricingPage from './pages/PricingPage';
import PaymentSuccess from './pages/PaymentSuccess';
import GlossaryPage from './pages/GlossaryPage';
import CertificatesPage from './pages/CertificatesPage';
import CertificatePage from './pages/CertificatePage';
import VerifyCertificatePage from './pages/VerifyCertificatePage';
import './App.css';

const AuthContext = React.createContext();

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');
    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const login = (userData, token) => {
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() {
  return React.useContext(AuthContext);
}

const LanguageContext = React.createContext();

function useLanguage() {
  return React.useContext(LanguageContext);
}

// Export context AND hook for use in other files
export { LanguageContext, useLanguage };

function LanguageProvider({ children }) {
  const { i18n } = useTranslation();
  // Load saved language or default to English
  const [language, setLanguageState] = useState(() => {
    return localStorage.getItem('app_language') || 'en-US';
  });
  const [displayMode, setDisplayMode] = useState('english');

  const setLanguage = (langCode) => {
    console.log('🌍 Changing language to:', langCode);
    setLanguageState(langCode);
    i18n.changeLanguage(langCode);
    localStorage.setItem('app_language', langCode); // Persist
    window.SELECTED_LANGUAGE = langCode; // Store globally
    
    // Force re-render by updating a timestamp
    window.dispatchEvent(new Event('languageChanged'));
  };

  // Initialize window.SELECTED_LANGUAGE and i18n on mount
  React.useEffect(() => {
    window.SELECTED_LANGUAGE = language;
    i18n.changeLanguage(language);
    console.log('🌍 Language initialized to:', language);
  }, [language, i18n]);

  return (
    <LanguageContext.Provider value={{ language, setLanguage, displayMode, setDisplayMode }}>
      {children}
    </LanguageContext.Provider>
  );
}

function Header() {
  const { user, logout } = useAuth();
  const { language, setLanguage, displayMode, setDisplayMode } = useLanguage();
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <header className="bg-primary text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold">
            STEAM Hub
          </Link>
          
          <nav className="flex items-center gap-4">
            <Link to="/lessons" className="hover:underline">
              {t('lessons')}
            </Link>
            <Link to="/calendar" className="hover:underline">
              {t('calendar')}
            </Link>
            {user && (
              <Link to="/dashboard" className="hover:underline">
                {t('dashboard')}
              </Link>
            )}
            {user && user.role === 'admin' && (
              <Link to="/admin" className="hover:underline">
                {t('admin')}
              </Link>
            )}
            <Link to="/inquiry" className="hover:underline">
              {t('contact')}
            </Link>
            <Link to="/pricing" className="hover:underline">
              Pricing
            </Link>
            <Link to="/glossary" className="hover:underline">
              Glossary
            </Link>
            
            <select 
              value={language} 
              onChange={(e) => {
                setLanguage(e.target.value);
                // Store in window for direct access
                window.SELECTED_LANGUAGE = e.target.value;
                console.log('🌍 Language changed to:', e.target.value);
              }}
              className="bg-white text-black px-2 py-1 rounded text-sm"
              id="language-selector"
            >
              {LANGUAGES.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.nativeName}
                </option>
              ))}
            </select>
            
            {/* Display Mode dropdown REMOVED - Always shows English Only */}
            
            {user ? (
              <div className="flex items-center gap-2">
                <span className="text-sm">{user.name}</span>
                <Button 
                  onClick={logout} 
                  variant="outline" 
                  size="sm"
                  className="bg-white text-primary"
                >
                  {t('logout')}
                </Button>
              </div>
            ) : (
              <div className="flex gap-2">
                <Button 
                  onClick={() => navigate('/login')} 
                  variant="outline" 
                  size="sm"
                  className="bg-white text-primary"
                >
                  {t('login')}
                </Button>
                <Button 
                  onClick={() => navigate('/register')} 
                  size="sm"
                  className="bg-white text-primary"
                >
                  {t('register')}
                </Button>
              </div>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}

function HomePage() {
  const navigate = useNavigate();
  const { t } = useTranslation();

  const ageGroups = [
    {
      age: '5-7',
      grade: 'K-2',
      title: 'Little Explorers',
      subtitle: 'Kindergarten to Grade 2',
      description: 'Fun, colorful lessons that introduce AI concepts through stories, games, and simple activities. Perfect for curious young minds!',
      lessons: '200+',
      icon: '🌱',
      bgClass: 'bg-[#E8F5E9]',
      borderClass: 'border-[#81C784]',
      textClass: 'text-[#2E7D32]',
      accentClass: 'bg-[#A5D6A7]',
      btnClass: 'bg-[#66BB6A] hover:bg-[#43A047] text-white',
    },
    {
      age: '8-9',
      grade: '3-4',
      title: 'Young Thinkers',
      subtitle: 'Grade 3 to Grade 4',
      description: 'Hands-on activities and real-world examples that build logical thinking. Learn how robots work and start simple coding!',
      lessons: '200+',
      icon: '🔬',
      bgClass: 'bg-[#E3F2FD]',
      borderClass: 'border-[#64B5F6]',
      textClass: 'text-[#1565C0]',
      accentClass: 'bg-[#90CAF9]',
      btnClass: 'bg-[#42A5F5] hover:bg-[#1E88E5] text-white',
    },
    {
      age: '10-12',
      grade: '5-7',
      title: 'Junior Scientists',
      subtitle: 'Grade 5 to Grade 7',
      description: 'Deeper understanding of AI, data, and technology. Project-based learning with creative problem-solving challenges!',
      lessons: '200+',
      icon: '🧪',
      bgClass: 'bg-[#F3E5F5]',
      borderClass: 'border-[#BA68C8]',
      textClass: 'text-[#7B1FA2]',
      accentClass: 'bg-[#CE93D8]',
      btnClass: 'bg-[#AB47BC] hover:bg-[#8E24AA] text-white',
    },
    {
      age: '13-15',
      grade: '8-10',
      title: 'Tech Innovators',
      subtitle: 'Grade 8 to Grade 10',
      description: 'Advanced AI concepts, machine learning basics, and ethical thinking. Prepare for the future of technology!',
      lessons: '200+',
      icon: '💡',
      bgClass: 'bg-[#FFF3E0]',
      borderClass: 'border-[#FFB74D]',
      textClass: 'text-[#E65100]',
      accentClass: 'bg-[#FFCC80]',
      btnClass: 'bg-[#FFA726] hover:bg-[#FB8C00] text-white',
    },
    {
      age: '16-18',
      grade: '11-12',
      title: 'Future Leaders',
      subtitle: 'Grade 11 to Grade 12',
      description: 'Research-level AI insights, career pathways, and real-world applications. Get ready for university and beyond!',
      lessons: '200+',
      icon: '🎓',
      bgClass: 'bg-[#FCE4EC]',
      borderClass: 'border-[#F48FB1]',
      textClass: 'text-[#AD1457]',
      accentClass: 'bg-[#F48FB1]',
      btnClass: 'bg-[#EC407A] hover:bg-[#D81B60] text-white',
    },
  ];

  return (
    <div className="min-h-screen bg-background" data-testid="home-page">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-primary/10 to-secondary/20">
        <div className="max-w-7xl mx-auto px-4 py-16 sm:py-20">
          <div className="text-center">
            <h1 className="text-5xl sm:text-6xl font-bold mb-4 tracking-tight" data-testid="home-title">
              Global STEAM Education Hub
            </h1>
            <p className="text-2xl text-muted-foreground mb-3" data-testid="home-welcome">
              {t('welcome')}
            </p>
            <p className="text-lg text-muted-foreground mb-8" data-testid="home-description">
              1,050+ AI &amp; STEAM Lessons &bull; Ages 5-18 &bull; 9+ Languages &bull; Free &amp; Premium Plans
            </p>
            <div className="flex gap-4 justify-center flex-wrap">
              <Button 
                size="lg" 
                onClick={() => navigate('/lessons')}
                data-testid="home-explore-lessons-btn"
              >
                {t('exploreLessons')}
              </Button>
              <Button 
                size="lg" 
                variant="outline"
                onClick={() => navigate('/register')}
                data-testid="home-get-started-btn"
              >
                {t('getStarted')}
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Browse by Age Section */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-10">
          <h2 className="text-3xl sm:text-4xl font-bold mb-3" data-testid="age-section-title">
            Choose Your Learning Path
          </h2>
          <p className="text-lg text-muted-foreground">
            Age-appropriate AI education designed by educators for young learners
          </p>
        </div>

        {/* Kids Sections (5-7, 8-9, 10-12) — Large Feature Cards */}
        <div className="space-y-6 mb-10">
          {ageGroups.slice(0, 3).map((group) => (
            <div 
              key={group.age}
              className={`rounded-2xl ${group.bgClass} border-2 ${group.borderClass} overflow-hidden transition-all duration-200 hover:shadow-xl cursor-pointer`}
              onClick={() => navigate(`/lessons?age=${group.age}`)}
              data-testid={`age-card-${group.age}`}
            >
              <div className="flex flex-col md:flex-row items-center gap-6 p-6 sm:p-8">
                {/* Left: Icon & Age */}
                <div className="flex flex-col items-center flex-shrink-0">
                  <div className={`w-20 h-20 sm:w-24 sm:h-24 rounded-full ${group.accentClass} flex items-center justify-center text-4xl sm:text-5xl shadow-sm`}>
                    {group.icon}
                  </div>
                  <div className={`mt-3 text-center`}>
                    <span className={`text-2xl sm:text-3xl font-bold ${group.textClass}`}>
                      Ages {group.age}
                    </span>
                    <p className="text-sm text-muted-foreground font-medium">
                      Grades {group.grade}
                    </p>
                  </div>
                </div>

                {/* Middle: Title & Description */}
                <div className="flex-1 text-center md:text-left">
                  <h3 className={`text-2xl sm:text-3xl font-bold ${group.textClass} mb-2`}>
                    {group.title}
                  </h3>
                  <p className="text-base text-foreground/80 leading-relaxed mb-3 max-w-2xl">
                    {group.description}
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center md:justify-start">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${group.accentClass} ${group.textClass}`}>
                      {group.lessons} Lessons
                    </span>
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${group.accentClass} ${group.textClass}`}>
                      Sinhala &amp; Tamil
                    </span>
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${group.accentClass} ${group.textClass}`}>
                      PDF Downloads
                    </span>
                  </div>
                </div>

                {/* Right: CTA */}
                <div className="flex-shrink-0">
                  <button 
                    className={`${group.btnClass} px-6 py-3 rounded-xl font-semibold text-base shadow-sm transition-all duration-200 transform hover:scale-105`}
                    data-testid={`age-explore-${group.age}-btn`}
                  >
                    Explore Lessons
                  </button>
                </div>
              </div>

              {/* Decorative watermark */}
              <div className="relative overflow-hidden">
                <div className={`absolute -bottom-4 -right-4 text-8xl font-black ${group.textClass} opacity-[0.04] select-none pointer-events-none`}>
                  STEAM
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Teens Sections (13-15, 16-18) — Compact Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          {ageGroups.slice(3).map((group) => (
            <div 
              key={group.age}
              className={`rounded-2xl ${group.bgClass} border-2 ${group.borderClass} p-6 transition-all duration-200 hover:shadow-xl cursor-pointer`}
              onClick={() => navigate(`/lessons?age=${group.age}`)}
              data-testid={`age-card-${group.age}`}
            >
              <div className="flex items-start gap-4">
                <div className={`w-14 h-14 rounded-full ${group.accentClass} flex items-center justify-center text-2xl flex-shrink-0 shadow-sm`}>
                  {group.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className={`text-xl font-bold ${group.textClass}`}>{group.title}</h3>
                    <span className="text-sm text-muted-foreground">Ages {group.age}</span>
                  </div>
                  <p className="text-sm text-foreground/80 leading-relaxed mb-3">
                    {group.description}
                  </p>
                  <button 
                    className={`${group.btnClass} px-4 py-2 rounded-lg font-semibold text-sm shadow-sm transition-all duration-200`}
                    data-testid={`age-explore-${group.age}-btn`}
                  >
                    Explore {group.lessons} Lessons
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="bg-muted/50 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {[
              { value: '1,050+', label: 'AI Lessons' },
              { value: '9+', label: 'Languages' },
              { value: '5', label: 'Age Groups' },
              { value: '20+', label: 'AI Topics' },
            ].map((stat, idx) => (
              <div key={idx}>
                <div className="text-3xl sm:text-4xl font-bold text-primary">{stat.value}</div>
                <div className="text-sm text-muted-foreground mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// Map frontend language codes to DB language codes
const LANG_CODE_MAP = {
  'en-US': 'en',
  'si-LK': 'si',
  'ta-IN': 'ta',
  'hi-IN': 'hi',
  'bn-IN': 'bn',
  'mr-IN': 'mr',
  'te-IN': 'te',
  'zh-CN': 'zh',
  'zh-HK': 'yue',
  'yue-HK': 'yue',
  'th-TH': 'th',
  'tl-PH': 'tl',
  'fil-PH': 'tl',
  'ms-MY': 'ms',
  'vi-VN': 'vi',
  'id-ID': 'id',
  'ur-PK': 'ur',
  'ar-SA': 'ar',
  'ja-JP': 'ja',
  'ko-KR': 'ko',
  'es-ES': 'es',
  'ru-RU': 'ru',
  'ne-NP': 'ne',
  'pa-IN': 'pa',
  'ps-AF': 'ps',
};

// Helper: get short language code from full code
const getDbLangCode = (fullCode) => LANG_CODE_MAP[fullCode] || 'en';

// Helper: get bilingual display text from lesson field (uses DB translations)
const getLocalizedText = (field, langCode) => {
  if (!field) return '';
  const dbCode = getDbLangCode(langCode);
  // If we have a translation in the DB for this language, use it
  if (dbCode !== 'en' && field[dbCode]) {
    return field[dbCode];
  }
  // Fallback to English
  return field.en || field.local || '';
};

function LessonsPage() {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    curriculum: '',
    subject: '',
    grade: '',
    query: '',
    age_group: ''
  });
  const { language, displayMode } = useLanguage();
  const { t } = useTranslation();
  const [initialized, setInitialized] = useState(false);

  // Read age filter from URL params on mount - BEFORE first load
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const ageParam = params.get('age');
    if (ageParam) {
      setFilters(prev => ({ ...prev, age_group: ageParam, curriculum: 'AI-STEAM' }));
    }
    setInitialized(true);
  }, []);

  useEffect(() => {
    if (initialized) {
      loadLessons();
    }
  }, [filters, initialized]);

  const loadLessons = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filters.curriculum) params.curriculum = filters.curriculum;
      if (filters.subject) params.subject = filters.subject;
      if (filters.grade) params.grade = filters.grade;
      if (filters.query) params.query = filters.query;
      if (filters.age_group) params.age_group = filters.age_group;
      
      const response = await api.getLessons(params);
      setLessons(response.data.lessons);
    } catch (error) {
      console.error('Error loading lessons:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDisplayText = (bilingualText) => {
    if (!bilingualText) return '';
    const dbCode = getDbLangCode(language);
    // Show DB translation if available
    if (dbCode !== 'en' && bilingualText[dbCode]) {
      return bilingualText[dbCode];
    }
    // Fallback
    return bilingualText.en || bilingualText.local || '';
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">{t('browseLessons')}</h1>
        
        <div className="mb-8 grid grid-cols-1 md:grid-cols-5 gap-4">
          <Input
            placeholder={t('searchLessons')}
            value={filters.query}
            onChange={(e) => setFilters({...filters, query: e.target.value})}
            data-testid="lesson-search-input"
          />
          
          <select 
            className="border rounded px-3 py-2"
            value={filters.curriculum}
            onChange={(e) => setFilters({...filters, curriculum: e.target.value})}
            data-testid="curriculum-filter"
          >
            <option value="">{t('allCurricula')}</option>
            <option value="AI-STEAM">AI &amp; STEAM</option>
            <option value="cambridge">Cambridge</option>
            <option value="edexcel">Edexcel</option>
            <option value="asdn">ASDN</option>
          </select>
          
          <select 
            className="border rounded px-3 py-2"
            value={filters.subject}
            onChange={(e) => setFilters({...filters, subject: e.target.value})}
            data-testid="subject-filter"
          >
            <option value="">{t('allSubjects')}</option>
            <option value="artificial_intelligence">Artificial Intelligence</option>
            <option value="mathematics">Mathematics</option>
            <option value="physics">Physics</option>
            <option value="chemistry">Chemistry</option>
            <option value="biology">Biology</option>
          </select>
          
          <select 
            className="border rounded px-3 py-2"
            value={filters.grade}
            onChange={(e) => setFilters({...filters, grade: e.target.value})}
            data-testid="grade-filter"
          >
            <option value="">{t('allGrades')}</option>
            <option value="K">Kindergarten (Age 5)</option>
            {[
              {grade: 1, age: '6-7'},
              {grade: 2, age: '7-8'},
              {grade: 3, age: '8-9'},
              {grade: 4, age: '9-10'},
              {grade: 5, age: '10-11'},
              {grade: 6, age: '11-12'},
              {grade: 7, age: '12-13'},
              {grade: 8, age: '13-14'},
              {grade: 9, age: '14-15'},
              {grade: 10, age: '15-16'},
              {grade: 11, age: '16-17'},
              {grade: 12, age: '17-18'}
            ].map(({grade, age}) => (
              <option key={grade} value={grade}>Grade {grade} (Age {age})</option>
            ))}
          </select>

          <select 
            className="border rounded px-3 py-2"
            value={filters.age_group || ''}
            onChange={(e) => {
              setFilters({...filters, age_group: e.target.value});
            }}
            data-testid="age-group-filter"
          >
            <option value="">All Age Groups</option>
            <option value="5-7">Ages 5-7 (K-2)</option>
            <option value="8-9">Ages 8-9 (3-4)</option>
            <option value="10-12">Ages 10-12 (5-7)</option>
            <option value="13-15">Ages 13-15 (8-10)</option>
            <option value="16-18">Ages 16-18 (11-12)</option>
          </select>
        </div>
        
        {loading ? (
          <div className="text-center py-20">{t('loading')}</div>
        ) : (
          <>
            {/* Age Group Banner - shows when specific age is selected */}
            {filters.age_group && (() => {
              const ageInfo = {
                '5-7': { title: 'Little Explorers', subtitle: 'Kindergarten to Grade 2', icon: '🌱', bg: 'bg-[#E8F5E9]', border: 'border-[#81C784]', text: 'text-[#2E7D32]', accent: 'bg-[#A5D6A7]' },
                '8-9': { title: 'Young Thinkers', subtitle: 'Grade 3 to Grade 4', icon: '🔬', bg: 'bg-[#E3F2FD]', border: 'border-[#64B5F6]', text: 'text-[#1565C0]', accent: 'bg-[#90CAF9]' },
                '10-12': { title: 'Junior Scientists', subtitle: 'Grade 5 to Grade 7', icon: '🧪', bg: 'bg-[#F3E5F5]', border: 'border-[#BA68C8]', text: 'text-[#7B1FA2]', accent: 'bg-[#CE93D8]' },
                '13-15': { title: 'Tech Innovators', subtitle: 'Grade 8 to Grade 10', icon: '💡', bg: 'bg-[#FFF3E0]', border: 'border-[#FFB74D]', text: 'text-[#E65100]', accent: 'bg-[#FFCC80]' },
                '16-18': { title: 'Future Leaders', subtitle: 'Grade 11 to Grade 12', icon: '🎓', bg: 'bg-[#FCE4EC]', border: 'border-[#F48FB1]', text: 'text-[#AD1457]', accent: 'bg-[#F48FB1]' },
              }[filters.age_group];
              
              return ageInfo ? (
                <div className={`${ageInfo.bg} ${ageInfo.border} border-2 rounded-2xl p-5 mb-6 flex items-center gap-4`} data-testid="age-banner">
                  <div className={`w-14 h-14 rounded-full ${ageInfo.accent} flex items-center justify-center text-3xl flex-shrink-0`}>
                    {ageInfo.icon}
                  </div>
                  <div>
                    <h2 className={`text-2xl font-bold ${ageInfo.text}`}>{ageInfo.title}</h2>
                    <p className="text-sm text-muted-foreground">{ageInfo.subtitle} &bull; Ages {filters.age_group} &bull; {lessons.length} lessons</p>
                  </div>
                  <div className={`ml-auto text-6xl font-black ${ageInfo.text} opacity-10 select-none hidden md:block`}>
                    STEAM
                  </div>
                </div>
              ) : null;
            })()}
          
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {lessons.map(lesson => (
              <Card key={lesson.id} className={`hover:shadow-lg transition-shadow duration-200 relative overflow-hidden ${
                lesson.age_group === '5-7' ? 'border-l-4 border-l-emerald-400 bg-emerald-50/30' :
                lesson.age_group === '8-9' ? 'border-l-4 border-l-sky-400 bg-sky-50/30' :
                lesson.age_group === '10-12' ? 'border-l-4 border-l-violet-400 bg-violet-50/30' :
                lesson.age_group === '13-15' ? 'border-l-4 border-l-amber-400 bg-amber-50/30' :
                lesson.age_group === '16-18' ? 'border-l-4 border-l-rose-400 bg-rose-50/30' : ''
              }`}>
                {/* Watermark for AI-STEAM lessons */}
                {lesson.curriculum === 'AI-STEAM' && (
                  <div className="absolute top-2 right-2 text-[10px] font-bold text-muted-foreground/20 rotate-0 pointer-events-none select-none tracking-widest uppercase">
                    STEAM Hub
                  </div>
                )}
                <CardHeader>
                  <div className="flex gap-2 mb-2 flex-wrap">
                    <Badge>{lesson.curriculum}</Badge>
                    <Badge variant="outline">Grade {lesson.grade}</Badge>
                    {lesson.term && <Badge variant="outline">Term {lesson.term}</Badge>}
                    {lesson.week && <Badge variant="outline">Week {lesson.week}</Badge>}
                    {lesson.age_group && <Badge variant="secondary">Ages {lesson.age_group}</Badge>}
                  </div>
                  <CardTitle className="text-lg">
                    {getDisplayText(lesson.title)}
                  </CardTitle>
                  {/* Show English subtitle when viewing in another language */}
                  {getDbLangCode(language) !== 'en' && lesson.title[getDbLangCode(language)] && (
                    <p className="text-sm text-muted-foreground italic mt-1">{lesson.title.en}</p>
                  )}
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">
                    {getDisplayText(lesson.description)}
                  </p>
                  <div className="flex gap-2">
                    <Button 
                      size="sm" 
                      onClick={() => window.location.href = '/lesson/' + lesson.id}
                      data-testid={`lesson-view-btn-${lesson.id}`}
                    >
                      {t('viewLesson')}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          </>
        )}
      </div>
    </div>
  );
}

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const { t } = useTranslation();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.login({ email, password });
      login(response.data.user, response.data.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-secondary">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>{t('login')}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <div className="text-red-500 text-sm">{error}</div>}
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <Input 
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Password</label>
              <Input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <Button type="submit" className="w-full">
              {t('login')}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const { login } = useAuth();
  const { t } = useTranslation();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.register(formData);
      login(response.data.user, response.data.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-secondary">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>{t('register')}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <div className="text-red-500 text-sm">{error}</div>}
            <div>
              <label className="block text-sm font-medium mb-1">Name</label>
              <Input 
                type="text" 
                value={formData.name} 
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <Input 
                type="email" 
                value={formData.email} 
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Password</label>
              <Input 
                type="password" 
                value={formData.password} 
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
              />
            </div>
            <Button type="submit" className="w-full">
              {t('register')}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [certSubject, setCertSubject] = useState('mathematics');
  const [certGrade, setCertGrade] = useState(7);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await api.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleGenerateCertificate = async () => {
    setGenerating(true);
    try {
      const response = await api.generateCertificate({
        curriculum: 'cambridge',
        subject: certSubject,
        grade: certGrade
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `certificate_${certSubject}_grade${certGrade}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('Certificate downloaded successfully!');
    } catch (error) {
      console.error('Error generating certificate:', error);
      toast.error('Error generating certificate. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  if (!stats) return <div className="p-8">Loading...</div>;

  // Prepare chart data
  const subjectData = [
    { name: 'Math', value: 35 },
    { name: 'Physics', value: 25 },
    { name: 'Chemistry', value: 20 },
    { name: 'Biology', value: 20 }
  ];

  const progressData = [
    { name: 'Week 1', completed: 2, inProgress: 1 },
    { name: 'Week 2', completed: 4, inProgress: 2 },
    { name: 'Week 3', completed: 6, inProgress: 3 },
    { name: 'Week 4', completed: 8, inProgress: 2 }
  ];

  const COLORS = ['#0891B2', '#10B981', '#F59E0B', '#EF4444'];

  const SUBJECTS = ['mathematics', 'physics', 'chemistry', 'biology', 'science', 'technology', 'engineering', 'arts', 'english', 'ict'];
  const GRADES = ['K', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Welcome, {user.name}!</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Total Lessons</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{stats.total_lessons}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Completed</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">{stats.completed_lessons}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">In Progress</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">{stats.in_progress_lessons}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Avg Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">{stats.average_quiz_score}%</div>
            </CardContent>
          </Card>
        </div>
        
        {/* Progress Charts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle>Learning Progress</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={progressData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="completed" fill="#10B981" name="Completed" />
                  <Bar dataKey="inProgress" fill="#0891B2" name="In Progress" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Subjects Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={subjectData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={entry => entry.name}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {subjectData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>
        
        {/* Enhanced Certificate Generation */}
        <Card>
          <CardHeader>
            <CardTitle>Generate Certificate</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Customize and download your completion certificate
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium mb-2">Subject</label>
                <select 
                  className="w-full border rounded px-3 py-2"
                  value={certSubject}
                  onChange={(e) => setCertSubject(e.target.value)}
                >
                  {SUBJECTS.map(s => (
                    <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Grade</label>
                <select 
                  className="w-full border rounded px-3 py-2"
                  value={certGrade}
                  onChange={(e) => setCertGrade(e.target.value)}
                >
                  {GRADES.map(g => (
                    <option key={g} value={g}>Grade {g}</option>
                  ))}
                </select>
              </div>
            </div>
            <Button 
              onClick={handleGenerateCertificate}
              disabled={generating}
            >
              {generating ? 'Generating...' : `Download ${certSubject.charAt(0).toUpperCase() + certSubject.slice(1)} Certificate`}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <LanguageProvider>
        <BrowserRouter>
          <div className="App">
            <Header />
            <Toaster />
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/lessons" element={<LessonsPage />} />
              <Route path="/calendar" element={<AcademicCalendar />} />
              <Route path="/lesson/:id" element={<LessonDetail />} />
              <Route path="/certificates" element={<CertificatesPage />} />
              <Route path="/certificate/:certNumber" element={<CertificatePage />} />
              <Route path="/verify/:certNumber" element={<VerifyCertificatePage />} />
              <Route path="/pricing" element={<PricingPage />} />
              <Route path="/payment-success" element={<PaymentSuccess />} />
              <Route path="/glossary" element={<GlossaryPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/admin" element={<AdminDashboard />} />
              <Route path="/inquiry" element={<InquiryForm />} />
            </Routes>
            
            <footer className="bg-muted/80 border-t py-8 mt-20" data-testid="app-footer">
              <div className="max-w-7xl mx-auto px-4 text-center">
                <div className="flex items-center justify-center gap-2 mb-3">
                  <span className="text-2xl font-bold text-primary tracking-tight">Global STEAM Education Hub</span>
                </div>
                <p className="text-sm font-semibold text-foreground mb-1">
                  Made by Education Reforms Bureau
                </p>
                <p className="text-xs text-muted-foreground">
                  &copy; {new Date().getFullYear()} TEC Sri Lanka Worldwide Pvt Ltd &bull; All Rights Reserved
                </p>
                <p className="text-xs text-muted-foreground mt-2">
                  Content adapted from OpenStax (CC BY 4.0) &amp; CK-12 (CC BY-NC 3.0)
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  K-12 AI &amp; STEAM Education &bull; Ages 5-18 &bull; 1,000+ Lessons &bull; 9+ Languages
                </p>
              </div>
            </footer>
          </div>
        </BrowserRouter>
      </LanguageProvider>
    </AuthProvider>
  );
}

export default App;
