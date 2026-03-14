import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../api';
import { speak, isRTL } from '../utils/tts';
import { Button } from '../components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Volume2, Play, FileText, Download, Share2, Mail, Copy, BookOpen, Globe } from 'lucide-react';
import { toast } from '../components/ui/sonner';
import { useLanguage } from '../App';

// Map frontend language codes to DB language codes
const LANG_CODE_MAP = {
  'en-US': 'en', 
  'si-LK': 'si', 
  'ta-IN': 'ta', 
  'hi-IN': 'hi',
  'zh-CN': 'zh', 
  'yue-HK': 'yue',
  'zh-HK': 'yue',
  'th-TH': 'th', 
  'vi-VN': 'vi', 
  'id-ID': 'id',
  'ms-MY': 'ms',
  'bn-IN': 'bn', 
  'ur-PK': 'ur', 
  'ar-SA': 'ar', 
  'ja-JP': 'ja',
  'ko-KR': 'ko', 
  'es-ES': 'es', 
  'ru-RU': 'ru', 
  'te-IN': 'te',
  'ne-NP': 'ne', 
  'pa-IN': 'pa', 
  'ps-AF': 'ps', 
  'fil-PH': 'tl',
  'tl-PH': 'tl',
  'mr-IN': 'mr',
};

const getDbLangCode = (fullCode) => {
  // Try direct mapping first
  if (LANG_CODE_MAP[fullCode]) {
    return LANG_CODE_MAP[fullCode];
  }
  // Try extracting just the language code (e.g., 'si' from 'si-LK')
  const shortCode = fullCode.split('-')[0];
  return shortCode || 'en';
};

// Auth context (keep local)
const AuthContext = React.createContext();

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    return { user };
  }
  return context;
}

function LessonDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { language } = useLanguage();
  const { user } = useAuth();
  const { t } = useTranslation();
  const [lesson, setLesson] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const [showQuiz, setShowQuiz] = useState(false);
  const [answers, setAnswers] = useState([]);
  const [quizResult, setQuizResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showBilingual, setShowBilingual] = useState(true); // Toggle: show English alongside native

  useEffect(() => {
    loadLesson();
    loadQuiz();
  }, [id]);

  const loadLesson = async () => {
    try {
      setLoading(true);
      const response = await api.getLesson(id);
      setLesson(response.data);
    } catch (error) {
      console.error('Error loading lesson:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadQuiz = async () => {
    try {
      const response = await api.getQuiz(id);
      setQuiz(response.data);
      setAnswers(new Array(response.data.questions.length).fill(null));
    } catch (error) {
      console.log('No quiz found for this lesson');
    }
  };

  // Get text in selected language from DB translations
  const getText = (field) => {
    if (!field) return '';
    const dbCode = getDbLangCode(language);
    if (dbCode !== 'en' && field[dbCode]) {
      return field[dbCode];
    }
    return field.en || field.local || '';
  };

  // Check if translation exists for current language
  const hasTranslation = (field) => {
    if (!field) return false;
    const dbCode = getDbLangCode(language);
    return dbCode !== 'en' && !!field[dbCode];
  };

  const getDisplayText = (bilingualText) => {
    if (!bilingualText) return '';
    return bilingualText.en || bilingualText.local || '';
  };

  const handleAnswerChange = (questionIndex, answerIndex) => {
    const newAnswers = [...answers];
    newAnswers[questionIndex] = answerIndex;
    setAnswers(newAnswers);
  };

  const handleSubmitQuiz = async () => {
    if (!user) {
      toast.error('Please login to take quizzes');
      return;
    }

    try {
      const response = await api.submitQuiz({
        lesson_id: id,
        user_id: user.id,
        answers: answers
      });
      setQuizResult(response.data);
      
      await api.updateProgress({
        lesson_id: id,
        status: response.data.passed ? 'completed' : 'in_progress',
        quiz_score: response.data.score
      });
      
      toast.success(`Quiz submitted! Score: ${response.data.score}%`);
    } catch (error) {
      console.error('Error submitting quiz:', error);
      toast.error('Error submitting quiz. Please try again.');
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/lessons/${id}/download`, {
        method: 'GET',
      });
      
      if (!response.ok) throw new Error('Download failed');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const safeTitle = (lesson.title.en || 'lesson').replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50);
      link.setAttribute('download', `lesson_${safeTitle}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Lesson downloaded successfully!');
    } catch (error) {
      console.error('Error downloading PDF:', error);
      toast.error('Error downloading lesson. Please try again.');
    }
  };

  const handleShareEmail = () => {
    const subject = encodeURIComponent(`Check out this lesson: ${lesson.title.en}`);
    const body = encodeURIComponent(`I found this great lesson on STEAM Hub!\n\n${lesson.title.en}\n${window.location.href}\n\nGlobal STEAM Education Hub - TEC Sri Lanka Worldwide`);
    window.location.href = `mailto:?subject=${subject}&body=${body}`;
  };

  const handleShareWhatsApp = () => {
    const text = encodeURIComponent(`Check out this lesson: ${lesson.title.en}\n${window.location.href}\n\nGlobal STEAM Education Hub`);
    window.open(`https://wa.me/?text=${text}`, '_blank');
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    toast.success('Link copied to clipboard!');
  };

  if (loading) return <div className="p-8 text-center">{t('loading')}</div>;
  if (!lesson) return <div className="p-8 text-center">Lesson not found</div>;

  const isTranslated = hasTranslation(lesson.title);
  const dbCode = getDbLangCode(language);

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Button onClick={() => navigate('/lessons')} variant="outline" className="mb-4" data-testid="back-to-lessons-btn">
          {t('backToLessons') || 'Back to Lessons'}
        </Button>

        <Card className="mb-8" data-testid="lesson-detail-card">
          <CardHeader>
            <div className="flex gap-2 mb-2 flex-wrap">
              <Badge data-testid="lesson-curriculum">{lesson.curriculum}</Badge>
              <Badge variant="outline" data-testid="lesson-grade">Grade {lesson.grade}</Badge>
              <Badge variant="outline" data-testid="lesson-subject">{lesson.subject}</Badge>
              {lesson.age_group && <Badge variant="secondary">Ages {lesson.age_group}</Badge>}
              {isTranslated && (
                <Badge variant="outline" className="text-primary border-primary" data-testid="translated-badge">
                  <Globe className="w-3 h-3 mr-1" />
                  Translated
                </Badge>
              )}
            </div>
            
            {/* Title with bilingual display */}
            <CardTitle className={`text-3xl mb-2 ${isRTL(language) ? 'text-right' : ''}`} data-testid="lesson-title">
              {getText(lesson.title)}
            </CardTitle>
            {isTranslated && showBilingual && (
              <p className="text-lg text-muted-foreground italic" data-testid="lesson-title-en">
                {lesson.title.en}
              </p>
            )}

            {/* Language toggle */}
            {isTranslated && (
              <div className="flex items-center gap-2 mt-3" data-testid="bilingual-toggle">
                <Button
                  size="sm"
                  variant={showBilingual ? "default" : "outline"}
                  onClick={() => setShowBilingual(!showBilingual)}
                  data-testid="toggle-bilingual-btn"
                >
                  <Globe className="w-4 h-4 mr-1" />
                  {showBilingual ? 'Hide English' : 'Show English'}
                </Button>
              </div>
            )}
          </CardHeader>
          
          <CardContent>
            {/* Action Buttons */}
            <div className="flex flex-wrap gap-2 mb-6 pb-4 border-b">
              <Button 
                size="default" 
                variant="default"
                onClick={() => {
                  // Read the entire lesson in selected language
                  const fullText = `${getText(lesson.title)}. ${getText(lesson.description)}. ${getText(lesson.content)}`;
                  speak(fullText, language);
                }}
                className="bg-green-600 hover:bg-green-700"
                data-testid="tts-read-lesson-btn"
              >
                <Volume2 className="w-5 h-5 mr-2" />
                🔊 {language === 'si-LK' ? 'පාඩම කියවන්න' : language === 'ta-IN' ? 'பாடத்தை படி' : language === 'hi-IN' ? 'पाठ पढ़ें' : 'Read Lesson'}
              </Button>

              <Button 
                size="sm" 
                variant="outline"
                onClick={handleDownloadPDF}
                data-testid="download-lesson-btn"
              >
                <Download className="w-4 h-4 mr-1" />
                Download PDF
              </Button>

              <Button 
                size="sm" 
                variant="outline"
                onClick={handleShareEmail}
                data-testid="share-email-btn"
              >
                <Mail className="w-4 h-4 mr-1" />
                Email
              </Button>

              <Button 
                size="sm" 
                variant="outline"
                onClick={handleShareWhatsApp}
                data-testid="share-whatsapp-btn"
              >
                <Share2 className="w-4 h-4 mr-1" />
                WhatsApp
              </Button>

              <Button 
                size="sm" 
                variant="outline"
                onClick={handleCopyLink}
                data-testid="copy-link-btn"
              >
                <Copy className="w-4 h-4 mr-1" />
                Copy Link
              </Button>
            </div>

            {/* Illustrations Section */}
            {lesson.illustration_url && (
              <div className="mb-6" data-testid="lesson-illustration-section">
                <h3 className="text-xl font-semibold mb-3 flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Illustration
                </h3>
                <img 
                  src={lesson.illustration_url} 
                  alt={`Illustration for ${lesson.title.en}`}
                  className="w-full max-w-2xl rounded-lg shadow-md"
                  loading="lazy"
                  data-testid="lesson-illustration-image"
                />
              </div>
            )}

            {/* Video Section */}
            {lesson.video_url && (
              <div className="mb-6" data-testid="lesson-video-section">
                <h3 className="text-xl font-semibold mb-3 flex items-center gap-2">
                  <Play className="w-5 h-5" />
                  Video
                </h3>
                <div className="aspect-video w-full max-w-2xl">
                  {lesson.video_url.includes('youtube.com') || lesson.video_url.includes('youtu.be') ? (
                    <iframe
                      src={lesson.video_url.replace('watch?v=', 'embed/')}
                      className="w-full h-full rounded-lg shadow-md"
                      frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                      title="Lesson video"
                      data-testid="lesson-video-iframe"
                    ></iframe>
                  ) : (
                    <video controls className="w-full h-full rounded-lg shadow-md" data-testid="lesson-video-player">
                      <source src={lesson.video_url} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  )}
                </div>
              </div>
            )}

            {/* Description */}
            <div className="mb-6" data-testid="lesson-description-section">
              <h3 className="text-xl font-semibold mb-2">{t('description') || 'Description'}</h3>
              <div className={isRTL(language) ? 'text-right' : ''}>
                <p className="text-base leading-relaxed">{getText(lesson.description)}</p>
                {isTranslated && showBilingual && (
                  <p className="text-sm text-muted-foreground italic mt-2">{lesson.description.en}</p>
                )}
              </div>
            </div>

            {/* Content */}
            <div className="mb-6" data-testid="lesson-content-section">
              <h3 className="text-xl font-semibold mb-2">{t('content') || 'Content'}</h3>
              <div className={isRTL(language) ? 'text-right' : ''}>
                <div className="prose max-w-none" 
                     dangerouslySetInnerHTML={{
                       __html: getText(lesson.content)
                         .replace(/###\s*/g, '\n\n###')  // Add breaks before headers
                         .replace(/##\s*/g, '\n\n##')    // Add breaks before headers
                         .replace(/-\s+/g, '\n- ')       // Add breaks before list items
                         .replace(/### (.*?)(?=\n|###|##|$)/g, '<h3 class="text-xl font-bold mt-4 mb-2">$1</h3>')
                         .replace(/## (.*?)(?=\n|###|##|$)/g, '<h2 class="text-2xl font-bold mt-6 mb-3">$1</h2>')
                         .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                         .replace(/\n/g, '<br/>')
                     }} 
                />
                {isTranslated && showBilingual && (
                  <div className="mt-4 pt-4 border-t">
                    <div className="prose prose-sm max-w-none text-muted-foreground"
                         dangerouslySetInnerHTML={{
                           __html: lesson.content.en
                             .replace(/### (.*?)(?=\n|$)/g, '<h3 class="text-lg font-bold mt-3 mb-2">$1</h3>')
                             .replace(/## (.*?)(?=\n|$)/g, '<h2 class="text-xl font-bold mt-4 mb-2">$1</h2>')
                             .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                             .replace(/\n/g, '<br/>')
                         }}
                    />
                  </div>
                )}
              </div>
            </div>

            {/* Attribution */}
            <div className="bg-muted p-4 rounded-lg" data-testid="lesson-attribution-section">
              <p className="text-sm text-muted-foreground">
                <strong>{t('source') || 'Source'}:</strong> {lesson.source} ({lesson.license})
              </p>
              {lesson.source_url && (
                <p className="text-sm text-muted-foreground mt-1">
                  <strong>URL:</strong> <a href={lesson.source_url} target="_blank" rel="noopener noreferrer" className="text-primary underline">{lesson.source_url}</a>
                </p>
              )}
              <p className="text-sm text-muted-foreground mt-1">
                <strong>{t('duration') || 'Duration'}:</strong> {lesson.estimated_duration} {t('minutes') || 'minutes'}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Quiz Section */}
        {quiz && (
          <Card data-testid="lesson-quiz-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5" />
                Quiz
              </CardTitle>
            </CardHeader>
            <CardContent>
              {!showQuiz ? (
                <div className="text-center py-8">
                  <p className="mb-4 text-muted-foreground">Test your knowledge with a quiz!</p>
                  <Button onClick={() => setShowQuiz(true)} data-testid="quiz-start-btn">Start Quiz</Button>
                </div>
              ) : quizResult ? (
                <div className="text-center py-8" data-testid="quiz-result-section">
                  <h3 className="text-3xl font-bold mb-4" data-testid="quiz-score">
                    Score: {quizResult.score}%
                  </h3>
                  <p className="text-lg mb-4" data-testid="quiz-status">
                    {quizResult.passed ? 'Passed!' : 'Keep Learning!'}
                  </p>
                  <p className="text-muted-foreground mb-4" data-testid="quiz-summary">
                    {quizResult.correct_answers} out of {quizResult.total_questions} correct
                  </p>
                  <div className="flex gap-4 justify-center">
                    <Button 
                      onClick={() => { setShowQuiz(false); setQuizResult(null); setAnswers(new Array(quiz.questions.length).fill(null)); }}
                      data-testid="quiz-retake-btn"
                    >
                      Retake Quiz
                    </Button>
                    <Button variant="outline" onClick={() => navigate('/dashboard')} data-testid="quiz-view-progress-btn">
                      View Progress
                    </Button>
                  </div>
                </div>
              ) : (
                <div data-testid="quiz-questions-section">
                  {quiz.questions.map((question, qIndex) => (
                    <div key={qIndex} className="mb-6 pb-6 border-b last:border-b-0" data-testid={`quiz-question-${qIndex}`}>
                      <h4 className="font-semibold mb-3">
                        {qIndex + 1}. {getDisplayText(question.question)}
                      </h4>
                      <div className="space-y-2">
                        {question.options.map((option, oIndex) => (
                          <label 
                            key={oIndex} 
                            className="flex items-center space-x-2 cursor-pointer hover:bg-muted p-2 rounded transition-colors"
                            data-testid={`quiz-option-${qIndex}-${oIndex}`}
                          >
                            <input
                              type="radio"
                              name={`question-${qIndex}`}
                              checked={answers[qIndex] === oIndex}
                              onChange={() => handleAnswerChange(qIndex, oIndex)}
                              className="w-4 h-4"
                            />
                            <span>{getDisplayText(option)}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  ))}
                  <Button 
                    onClick={handleSubmitQuiz} 
                    className="w-full"
                    disabled={answers.some(a => a === null)}
                    data-testid="quiz-submit-btn"
                  >
                    Submit Quiz
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}

export default LessonDetail;
