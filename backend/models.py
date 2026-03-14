from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    password_hash: str
    role: str = "student"  # student or admin
    name: str
    preferred_language: str = "en-US"
    display_mode: str = "bilingual"  # bilingual, local, english
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: Optional[str] = "student"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class BilingualText(BaseModel):
    en: str
    local: str

class Lesson(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: BilingualText
    description: BilingualText
    content: BilingualText
    curriculum: str  # cambridge, edexcel, asdn
    subject: str  # mathematics, physics, chemistry, biology, science, technology, engineering, arts, english, ict
    grade: int  # K-12 (K=0, 1-12)
    term: int  # 1, 2, or 3
    week: int  # 1-12 (week within the term)
    language_code: str  # for TTS
    difficulty: str = "medium"  # easy, medium, hard
    estimated_duration: int = 30  # minutes (age-appropriate)
    source: str  # OpenStax, CK-12, Khan Academy, etc.
    license: str  # CC BY 4.0, CC BY-NC 3.0
    source_url: Optional[str] = None
    illustration_url: Optional[str] = None  # Educational illustration
    video_url: Optional[str] = None  # Educational video (Khan Academy, YouTube EDU)
    interactive_url: Optional[str] = None  # PhET simulations, GeoGebra, etc.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LessonCreate(BaseModel):
    title: BilingualText
    description: BilingualText
    content: BilingualText
    curriculum: str
    subject: str
    grade: int
    term: int
    week: int
    language_code: str
    difficulty: Optional[str] = "medium"
    estimated_duration: Optional[int] = 30
    source: str
    license: str
    source_url: Optional[str] = None
    illustration_url: Optional[str] = None
    video_url: Optional[str] = None
    interactive_url: Optional[str] = None

class Question(BaseModel):
    question: BilingualText
    options: List[BilingualText]
    correct_answer: int
    explanation: BilingualText
    difficulty: str = "medium"

class Quiz(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    lesson_id: str
    questions: List[Question]
    passing_score: int = 70
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuizSubmission(BaseModel):
    lesson_id: str
    user_id: str
    answers: List[int]
    score: Optional[int] = None
    passed: Optional[bool] = None
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Progress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    lesson_id: str
    status: str = "in_progress"  # not_started, in_progress, completed
    quiz_score: Optional[int] = None
    time_spent: int = 0  # minutes
    last_accessed: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class ProgressUpdate(BaseModel):
    lesson_id: str
    status: Optional[str] = None
    quiz_score: Optional[int] = None
    time_spent: Optional[int] = None

class Inquiry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    organization: Optional[str] = None
    curriculum: str
    grade_range: str
    num_students: Optional[int] = None
    message: str
    status: str = "new"  # new, contacted, converted, archived
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None

class InquiryCreate(BaseModel):
    name: str
    email: EmailStr
    organization: Optional[str] = None
    curriculum: str
    grade_range: str
    num_students: Optional[int] = None
    message: str

class Certificate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    curriculum: str
    subject: str
    grade: int
    completion_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    certificate_url: Optional[str] = None