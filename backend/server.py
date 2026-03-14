from fastapi import FastAPI, APIRouter, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel as PydanticBaseModel

from models import (
    User, UserCreate, UserLogin, TokenResponse,
    Lesson, LessonCreate, Quiz, QuizSubmission,
    Progress, ProgressUpdate, Inquiry, InquiryCreate,
    Certificate, BilingualText
)
from database import (
    db, users_collection, lessons_collection, quizzes_collection,
    progress_collection, inquiries_collection, certificates_collection,
    serialize_doc
)
from auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_admin
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Global STEAM Education Hub API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Global STEAM Education Hub API"}

# Authentication endpoints
@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        name=user_data.name,
        role=user_data.role or "student"
    )
    
    user_dict = user.model_dump()
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    
    await users_collection.insert_one(user_dict)
    
    # Create access token
    token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role}
    )
    
    user_response = user.model_dump()
    del user_response['password_hash']
    
    return TokenResponse(access_token=token, user=user_response)

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    # Find user
    user_doc = await users_collection.find_one({"email": credentials.email})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(credentials.password, user_doc['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    token = create_access_token(
        data={"sub": user_doc['id'], "email": user_doc['email'], "role": user_doc['role']}
    )
    
    user_response = serialize_doc(user_doc)
    del user_response['password_hash']
    
    return TokenResponse(access_token=token, user=user_response)

# Lessons endpoints
@api_router.get("/lessons")
async def get_lessons(
    curriculum: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    grade: Optional[int] = Query(None),
    language: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    age_group: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100)
):
    # Build filter
    filters = {}
    if curriculum:
        filters['curriculum'] = curriculum
    if subject:
        filters['subject'] = subject
    if grade:
        filters['grade'] = grade
    if language:
        filters['language_code'] = language
    if age_group:
        filters['age_group'] = age_group
    
    # Get lessons - sort by ID to show random variety instead of alphabetical repetition
    # This prevents showing 5 versions of same lesson (different grades) consecutively
    cursor = lessons_collection.find(filters, {"_id": 0}).sort([("id", 1)])
    
    # Apply pagination
    cursor = cursor.skip(skip).limit(limit)
    
    lessons = await cursor.to_list(length=limit)
    
    # Filter by query if provided
    if query and lessons:
        query_lower = query.lower()
        lessons = [
            lesson for lesson in lessons
            if query_lower in lesson.get('title', {}).get('en', '').lower()
            or query_lower in lesson.get('title', {}).get('local', '').lower()
            or query_lower in lesson.get('description', {}).get('en', '').lower()
        ]
    
    return {"lessons": serialize_doc(lessons), "count": len(lessons)}

@api_router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str):
    lesson = await lessons_collection.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return serialize_doc(lesson)

@api_router.post("/lessons", dependencies=[Depends(require_admin)])
async def create_lesson(lesson_data: LessonCreate):
    lesson = Lesson(**lesson_data.model_dump())
    lesson_dict = lesson.model_dump()
    lesson_dict['created_at'] = lesson_dict['created_at'].isoformat()
    lesson_dict['updated_at'] = lesson_dict['updated_at'].isoformat()
    
    await lessons_collection.insert_one(lesson_dict)
    return serialize_doc(lesson_dict)

@api_router.put("/lessons/{lesson_id}", dependencies=[Depends(require_admin)])
async def update_lesson(lesson_id: str, lesson_data: LessonCreate):
    lesson_dict = lesson_data.model_dump()
    lesson_dict['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    result = await lessons_collection.update_one(
        {"id": lesson_id},
        {"$set": lesson_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    updated_lesson = await lessons_collection.find_one({"id": lesson_id}, {"_id": 0})
    return serialize_doc(updated_lesson)

@api_router.delete("/lessons/{lesson_id}", dependencies=[Depends(require_admin)])
async def delete_lesson(lesson_id: str):
    result = await lessons_collection.delete_one({"id": lesson_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"message": "Lesson deleted successfully"}

# Quiz endpoints
@api_router.get("/quiz/{lesson_id}")
async def get_quiz(lesson_id: str):
    quiz = await quizzes_collection.find_one({"lesson_id": lesson_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found for this lesson")
    return serialize_doc(quiz)

@api_router.post("/quiz/submit")
async def submit_quiz(
    submission: QuizSubmission,
    current_user: dict = Depends(get_current_user)
):
    # Get quiz
    quiz = await quizzes_collection.find_one({"lesson_id": submission.lesson_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz['questions'])
    
    for i, answer in enumerate(submission.answers):
        if i < len(quiz['questions']) and answer == quiz['questions'][i]['correct_answer']:
            correct_answers += 1
    
    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    passed = score >= quiz.get('passing_score', 70)
    
    # Update progress
    await progress_collection.update_one(
        {"user_id": current_user['sub'], "lesson_id": submission.lesson_id},
        {
            "$set": {
                "quiz_score": score,
                "status": "completed" if passed else "in_progress",
                "last_accessed": datetime.now(timezone.utc).isoformat(),
                "completed_at": datetime.now(timezone.utc).isoformat() if passed else None
            }
        },
        upsert=True
    )
    
    return {
        "score": score,
        "passed": passed,
        "correct_answers": correct_answers,
        "total_questions": total_questions
    }

# Progress endpoints
@api_router.get("/progress/{user_id}")
async def get_progress(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    # Users can only see their own progress unless they're admin
    if current_user['sub'] != user_id and current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to view this progress")
    
    progress_list = await progress_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ).to_list(length=1000)
    
    return {"progress": serialize_doc(progress_list)}

@api_router.post("/progress/update")
async def update_progress(
    progress_data: ProgressUpdate,
    current_user: dict = Depends(get_current_user)
):
    update_fields = {"last_accessed": datetime.now(timezone.utc).isoformat()}
    
    if progress_data.status:
        update_fields['status'] = progress_data.status
        if progress_data.status == 'completed':
            update_fields['completed_at'] = datetime.now(timezone.utc).isoformat()
    
    if progress_data.quiz_score is not None:
        update_fields['quiz_score'] = progress_data.quiz_score
    
    if progress_data.time_spent is not None:
        update_fields['time_spent'] = progress_data.time_spent
    
    await progress_collection.update_one(
        {"user_id": current_user['sub'], "lesson_id": progress_data.lesson_id},
        {
            "$set": update_fields,
            "$setOnInsert": {
                "id": str(__import__('uuid').uuid4()),
                "user_id": current_user['sub'],
                "lesson_id": progress_data.lesson_id
            }
        },
        upsert=True
    )
    
    return {"message": "Progress updated successfully"}

# Inquiries endpoints
@api_router.post("/inquiries")
async def create_inquiry(inquiry_data: InquiryCreate):
    inquiry = Inquiry(**inquiry_data.model_dump())
    inquiry_dict = inquiry.model_dump()
    inquiry_dict['created_at'] = inquiry_dict['created_at'].isoformat()
    
    await inquiries_collection.insert_one(inquiry_dict)
    return {"message": "Inquiry submitted successfully", "id": inquiry.id}

@api_router.get("/admin/inquiries", dependencies=[Depends(require_admin)])
async def get_inquiries(
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=200)
):
    filters = {}
    if status:
        filters['status'] = status
    
    inquiries = await inquiries_collection.find(
        filters,
        {"_id": 0}
    ).skip(skip).limit(limit).to_list(length=limit)
    
    return {"inquiries": serialize_doc(inquiries), "count": len(inquiries)}

@api_router.put("/admin/inquiries/{inquiry_id}", dependencies=[Depends(require_admin)])
async def update_inquiry(inquiry_id: str, status: str, notes: Optional[str] = None):
    update_fields = {"status": status}
    if notes:
        update_fields['notes'] = notes
    
    result = await inquiries_collection.update_one(
        {"id": inquiry_id},
        {"$set": update_fields}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    return {"message": "Inquiry updated successfully"}

# Statistics endpoint
@api_router.get("/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    total_lessons = await lessons_collection.count_documents({})
    
    user_progress = await progress_collection.find(
        {"user_id": current_user['sub']}
    ).to_list(length=1000)
    
    completed = sum(1 for p in user_progress if p.get('status') == 'completed')
    in_progress = sum(1 for p in user_progress if p.get('status') == 'in_progress')
    
    avg_score = 0
    scores = [p.get('quiz_score') for p in user_progress if p.get('quiz_score') is not None]
    if scores:
        avg_score = sum(scores) / len(scores)
    
    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed,
        "in_progress_lessons": in_progress,
        "average_quiz_score": round(avg_score, 1)
    }

# Certificates endpoint
@api_router.post("/certificates/generate")
async def generate_certificate(
    curriculum: str,
    subject: str,
    grade: int,
    current_user: dict = Depends(get_current_user)
):
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    import io
    from fastapi.responses import StreamingResponse
    
    # Create PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Certificate design
    # Border
    c.setStrokeColor(colors.HexColor('#0891B2'))
    c.setLineWidth(3)
    c.rect(0.5*inch, 0.5*inch, width-1*inch, height-1*inch)
    
    # Title
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(colors.HexColor('#0891B2'))
    c.drawCentredString(width/2, height-2*inch, "Certificate of Completion")
    
    # Body text
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height-3*inch, "This is to certify that")
    
    # Student name
    user_doc = await users_collection.find_one({"id": current_user['sub']})
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#0891B2'))
    c.drawCentredString(width/2, height-3.7*inch, user_doc.get('name', 'Student'))
    
    # Completion text
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height-4.5*inch, "has successfully completed")
    
    # Course details
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor('#0891B2'))
    course_text = f"{subject.title()} - Grade {grade}"
    c.drawCentredString(width/2, height-5.3*inch, course_text)
    
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height-5.8*inch, f"Curriculum: {curriculum.upper()}")
    
    # Date
    from datetime import datetime
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-7*inch, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.gray)
    c.drawCentredString(width/2, 1.2*inch, "Global STEAM Education Hub")
    c.drawCentredString(width/2, 1*inch, "TEC Sri Lanka Worldwide")
    
    c.save()
    buffer.seek(0)
    
    # Save to database
    cert = {
        "id": str(__import__('uuid').uuid4()),
        "user_id": current_user['sub'],
        "curriculum": curriculum,
        "subject": subject,
        "grade": grade,
        "completion_date": datetime.now(timezone.utc).isoformat()
    }
    await certificates_collection.insert_one(cert)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=certificate_{subject}_{grade}.pdf"}
    )


# Download Lesson as PDF endpoint
@api_router.get("/lessons/{lesson_id}/download")
async def download_lesson_pdf(lesson_id: str):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    import io
    from fastapi.responses import StreamingResponse
    
    # Get lesson
    lesson = await lessons_collection.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson = serialize_doc(lesson)
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0891B2'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#0891B2'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=12,
        leading=18,
        spaceAfter=12
    )
    
    # Add title
    title_text = lesson.get('title', {}).get('en', 'Lesson')
    title = Paragraph(title_text, title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Add metadata
    metadata = [
        f"<b>Curriculum:</b> {lesson.get('curriculum', 'N/A').upper()}",
        f"<b>Grade:</b> {lesson.get('grade', 'N/A')}",
        f"<b>Subject:</b> {lesson.get('subject', 'N/A').title()}",
        f"<b>Difficulty:</b> {lesson.get('difficulty', 'N/A').title()}",
        f"<b>Duration:</b> {lesson.get('estimated_duration', 'N/A')} minutes"
    ]
    
    for meta in metadata:
        elements.append(Paragraph(meta, body_style))
    
    elements.append(Spacer(1, 20))
    
    # Add description
    desc_heading = Paragraph("Description", heading_style)
    elements.append(desc_heading)
    desc_text = lesson.get('description', {}).get('en', 'No description available')
    desc = Paragraph(desc_text, body_style)
    elements.append(desc)
    elements.append(Spacer(1, 20))
    
    # Add content
    content_heading = Paragraph("Lesson Content", heading_style)
    elements.append(content_heading)
    content_text = lesson.get('content', {}).get('en', 'No content available')
    content = Paragraph(content_text, body_style)
    elements.append(content)
    elements.append(Spacer(1, 20))
    
    # Add attribution
    attribution_heading = Paragraph("Attribution & Licensing", heading_style)
    elements.append(attribution_heading)
    
    attribution_text = f"""
    <b>Source:</b> {lesson.get('source', 'N/A')} ({lesson.get('license', 'N/A')})<br/>
    <b>URL:</b> {lesson.get('source_url', 'N/A')}<br/>
    <br/>
    <i>Downloaded from Global STEAM Education Hub<br/>
    TEC Sri Lanka Worldwide © 2024</i>
    """
    attribution = Paragraph(attribution_text, body_style)
    elements.append(attribution)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Create safe filename
    safe_title = lesson.get('title', {}).get('en', 'lesson').replace(' ', '_').replace('/', '_')[:50]
    filename = f"lesson_{safe_title}.pdf"
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ==========================================
# STRIPE PAYMENT INTEGRATION
# ==========================================
from emergentintegrations.payments.stripe.checkout import (
    StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
)

# Fixed subscription packages (NEVER accept amount from frontend)
SUBSCRIPTION_PACKAGES = {
    "standard": {"amount": 5.00, "currency": "usd", "name": "Standard Plan", "lkr_price": 1500},
    "premium": {"amount": 10.00, "currency": "usd", "name": "Premium Plan", "lkr_price": 3000},
}

payment_transactions_collection = db.payment_transactions

class SubscribeRequest(PydanticBaseModel):
    package_id: str
    origin_url: str

@api_router.get("/stripe/publishable-key")
async def get_stripe_publishable_key():
    """Return the publishable key for the frontend"""
    key = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
    return {"publishable_key": key}

@api_router.post("/stripe/create-checkout")
async def create_checkout_session(req: SubscribeRequest, http_request: Request = None):
    """Create a Stripe checkout session for subscription"""
    # Validate package
    if req.package_id not in SUBSCRIPTION_PACKAGES:
        raise HTTPException(status_code=400, detail=f"Invalid package: {req.package_id}")
    
    package = SUBSCRIPTION_PACKAGES[req.package_id]
    
    # Get Stripe API key
    stripe_api_key = os.getenv('STRIPE_API_KEY')
    if not stripe_api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    # Build URLs from frontend origin (NEVER hardcode)
    success_url = f"{req.origin_url}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{req.origin_url}/pricing"
    
    # Setup webhook
    host_url = str(http_request.base_url).rstrip('/') if http_request else req.origin_url
    webhook_url = f"{host_url}/api/webhook/stripe"
    
    stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
    
    # Create checkout session
    checkout_request = CheckoutSessionRequest(
        amount=package["amount"],
        currency=package["currency"],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "package_id": req.package_id,
            "package_name": package["name"],
        }
    )
    
    try:
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create payment transaction record
        import uuid as uuid_mod
        transaction = {
            "id": str(uuid_mod.uuid4()),
            "session_id": session.session_id,
            "package_id": req.package_id,
            "package_name": package["name"],
            "amount": package["amount"],
            "currency": package["currency"],
            "payment_status": "initiated",
            "status": "pending",
            "metadata": {"package_id": req.package_id},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await payment_transactions_collection.insert_one(transaction)
        
        return {"url": session.url, "session_id": session.session_id}
    except Exception as e:
        logger.error(f"Stripe checkout error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Payment error: {str(e)}")

@api_router.get("/stripe/checkout-status/{session_id}")
async def get_checkout_status(session_id: str):
    """Check status of a checkout session"""
    stripe_api_key = os.getenv('STRIPE_API_KEY')
    if not stripe_api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url="")
    
    try:
        status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        # Update transaction in database (only once)
        existing = await payment_transactions_collection.find_one({"session_id": session_id})
        if existing and existing.get("payment_status") != "paid":
            await payment_transactions_collection.update_one(
                {"session_id": session_id},
                {"$set": {
                    "payment_status": status.payment_status,
                    "status": status.status,
                    "amount_total": status.amount_total,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }}
            )
        
        return {
            "status": status.status,
            "payment_status": status.payment_status,
            "amount_total": status.amount_total,
            "currency": status.currency,
        }
    except Exception as e:
        logger.error(f"Checkout status error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    stripe_api_key = os.getenv('STRIPE_API_KEY')
    if not stripe_api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    
    host_url = str(request.base_url).rstrip('/')
    webhook_url = f"{host_url}api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
    
    try:
        body = await request.body()
        signature = request.headers.get("Stripe-Signature", "")
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        # Update transaction
        if webhook_response and webhook_response.session_id:
            await payment_transactions_collection.update_one(
                {"session_id": webhook_response.session_id},
                {"$set": {
                    "payment_status": webhook_response.payment_status,
                    "event_type": webhook_response.event_type,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }}
            )
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return {"status": "error", "detail": str(e)}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Google Cloud Text-to-Speech endpoint
from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    language: str = "en-US"

@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech using Azure TTS (for Sinhala) or Google Cloud TTS (for others)
    Returns base64 encoded audio
    """
    import requests
    
    try:
        # DEBUG: Log exactly what we receive
        logger.info(f"🔊 TTS REQUEST: language={request.language}, text={request.text[:30]}...")
        
        # Use Azure for Sinhala, Google Cloud for others
        if request.language == 'si-LK':
            logger.info("→ Routing to AZURE for Sinhala")
            return await azure_tts(request.text, request.language)
        else:
            logger.info(f"→ Routing to GOOGLE for {request.language}")
            return await google_tts(request.text, request.language)
            
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def azure_tts(text: str, language: str):
    """Azure Speech Service TTS for Sinhala"""
    import requests
    
    api_key = os.getenv('AZURE_SPEECH_KEY')
    region = os.getenv('AZURE_SPEECH_REGION')
    
    if not api_key or not region:
        raise HTTPException(status_code=500, detail="Azure TTS not configured")
    
    logger.info(f"Azure TTS: language={language}, text={text[:50]}...")
    
    # Voice mapping
    voice_map = {
        'si-LK': 'si-LK-ThiliniNeural',  # Sinhala female voice
    }
    
    voice_name = voice_map.get(language, 'en-US-JennyNeural')
    
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3'
    }
    
    ssml = f"""<speak version='1.0' xml:lang='si-LK'>
        <voice xml:lang='si-LK' name='{voice_name}'>
            {text}
        </voice>
    </speak>"""
    
    response = requests.post(url, headers=headers, data=ssml.encode('utf-8'))
    
    if response.status_code == 200:
        import base64
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        logger.info("✅ Azure TTS audio generated successfully")
        return {"audio": audio_base64, "success": True}
    else:
        logger.error(f"Azure TTS error: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

async def google_tts(text: str, language: str):
    """Google Cloud TTS for Tamil, Hindi, etc."""
    import requests
    
    api_key = os.getenv('GOOGLE_CLOUD_TTS_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="Google TTS API key not configured")
    
    logger.info(f"Google TTS: language={language}, text={text[:50]}...")
    
    # Map language codes to Google Cloud TTS voice names
    voice_map = {
        'ta-IN': {'languageCode': 'ta-IN', 'name': 'ta-IN-Standard-A'},
        'hi-IN': {'languageCode': 'hi-IN', 'name': 'hi-IN-Standard-A'},
        'ar-SA': {'languageCode': 'ar-XA', 'name': 'ar-XA-Standard-A'},
        'bn-IN': {'languageCode': 'bn-IN', 'name': 'bn-IN-Standard-A'},
        'en-US': {'languageCode': 'en-US', 'name': 'en-US-Standard-A'},
    }
    
    voice_config = voice_map.get(language, {'languageCode': 'en-US', 'name': 'en-US-Standard-A'})
    
    logger.info(f"Using Google voice: {voice_config}")
    
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": voice_config['languageCode'],
            "name": voice_config['name']
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "pitch": 0,
            "speakingRate": 0.9
        }
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        audio_content = response.json().get('audioContent')
        logger.info("✅ Google TTS audio generated successfully")
        return {"audio": audio_content, "success": True}
    else:
        logger.error(f"Google TTS error: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.on_event("shutdown")
async def shutdown_db_client():
    from database import client
    client.close()

# ==========================================
# TEXT-TO-SPEECH (Google Translate TTS Proxy)
# ==========================================
import httpx

@api_router.post("/tts")
async def text_to_speech(request: Request):
    """Proxy Google Translate TTS for Sinhala/Tamil/etc voice reading"""
    import base64
    body = await request.json()
    text = body.get("text", "")
    lang = body.get("language", "en")
    
    # Map frontend codes to Google TTS codes
    lang_map = {
        "si-LK": "si", "ta-IN": "ta", "hi-IN": "hi", "zh-CN": "zh-CN",
        "zh-HK": "zh-TW", "th-TH": "th", "vi-VN": "vi", "id-ID": "id",
        "bn-IN": "bn", "ur-PK": "ur", "ar-SA": "ar", "en-US": "en",
        "ja-JP": "ja", "ko-KR": "ko", "ru-RU": "ru",
    }
    tts_lang = lang_map.get(lang, lang.split("-")[0])
    
    if not text or len(text.strip()) < 2:
        return {"success": False, "error": "No text provided"}
    
    # Split into chunks (Google TTS limit ~200 chars)
    chunks = []
    sentences = text.replace("\n", ". ").split(". ")
    current = ""
    for s in sentences:
        if len(current + s) > 180:
            if current.strip():
                chunks.append(current.strip())
            current = s
        else:
            current = current + ". " + s if current else s
    if current.strip():
        chunks.append(current.strip())
    
    # Fetch audio for each chunk
    audio_parts = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        for chunk in chunks[:20]:  # Max 20 chunks
            try:
                encoded = httpx.QueryParams({"ie": "UTF-8", "q": chunk, "tl": tts_lang, "client": "tw-ob"})
                url = f"https://translate.google.com/translate_tts?{encoded}"
                resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 200:
                    audio_parts.append(resp.content)
            except Exception as e:
                logger.warning(f"TTS chunk error: {e}")
    
    if audio_parts:
        combined = b"".join(audio_parts)
        audio_b64 = base64.b64encode(combined).decode()
        return {"success": True, "audio": audio_b64, "language": tts_lang}
    
    return {"success": False, "error": "TTS generation failed"}

# ============= CERTIFICATE SYSTEM =============

@api_router.get("/certificates/progress")
async def get_certificate_progress(current_user: dict = Depends(get_current_user)):
    """Get user's certificate progress by age group"""
    user_id = current_user['sub']
    
    age_groups = ['5-7', '8-9', '10-12', '13-15', '16-18']
    progress = []
    
    for age_group in age_groups:
        total_lessons = await lessons_collection.count_documents({
            'is_ai_curriculum': True,
            'age_group': age_group
        })
        
        completed = await progress_collection.count_documents({
            'user_id': user_id,
            'age_group': age_group,
            'completed': True
        })
        
        cert = await certificates_collection.find_one({
            'user_id': user_id,
            'age_group': age_group
        })
        
        progress.append({
            'age_group': age_group,
            'total_lessons': total_lessons,
            'completed_lessons': completed,
            'progress_percentage': (completed / total_lessons * 100) if total_lessons > 0 else 0,
            'certificate_number': cert['certificate_number'] if cert else None,
            'certificate_status': cert['status'] if cert else 'not_requested',
            'unlocked': completed >= (total_lessons * 0.8)
        })
    
    return {'progress': progress}


@api_router.post("/certificates/request")
async def request_certificate(age_group: str, current_user: dict = Depends(get_current_user)):
    """Request a certificate for completed age group"""
    user_id = current_user['sub']
    
    total_lessons = await lessons_collection.count_documents({
        'is_ai_curriculum': True,
        'age_group': age_group
    })
    
    completed = await progress_collection.count_documents({
        'user_id': user_id,
        'age_group': age_group,
        'completed': True
    })
    
    if completed < (total_lessons * 0.8):
        raise HTTPException(
            status_code=400,
            detail=f"Complete at least 80% of lessons ({completed}/{total_lessons})"
        )
    
    existing = await certificates_collection.find_one({
        'user_id': user_id,
        'age_group': age_group
    })
    
    if existing:
        return {'message': 'Certificate exists', 'certificate_number': existing['certificate_number']}
    
    count = await certificates_collection.count_documents({})
    cert_number = f"CERT-{datetime.now().year}-{str(count + 1).zfill(6)}"
    
    user_doc = await users_collection.find_one({'id': user_id})
    
    certificate = {
        'id': str(uuid.uuid4()),
        'certificate_number': cert_number,
        'user_id': user_id,
        'student_name': user_doc.get('name', 'Student'),
        'age_group': age_group,
        'program': 'AI & STEAM Education',
        'total_lessons': total_lessons,
        'completed_lessons': completed,
        'status': 'approved',
        'requested_date': datetime.now(timezone.utc).isoformat(),
        'approved_date': datetime.now(timezone.utc).isoformat()
    }
    
    await certificates_collection.insert_one(certificate)
    
    return {'message': 'Certificate approved!', 'certificate_number': cert_number}


@api_router.get("/certificates/{cert_number}")
async def get_certificate(cert_number: str):
    """Get certificate details"""
    import qrcode
    import io
    import base64
    
    cert = await certificates_collection.find_one(
        {'certificate_number': cert_number},
        {'_id': 0}
    )
    
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    verify_url = f"https://cert-verify-global.preview.emergentagent.com/verify/{cert_number}"
    qr.add_data(verify_url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    cert['qr_code'] = f"data:image/png;base64,{qr_base64}"
    cert['verification_url'] = verify_url
    
    return cert


@api_router.get("/verify/{cert_number}")
async def verify_certificate(cert_number: str):
    """Public certificate verification"""
    cert = await certificates_collection.find_one(
        {'certificate_number': cert_number},
        {'_id': 0, 'id': 0, 'user_id': 0}
    )
    
    if not cert:
        return {'valid': False, 'message': 'Certificate not found'}
    
    if cert['status'] != 'approved':
        return {'valid': False, 'message': 'Certificate not approved'}
    
    return {'valid': True, 'message': 'Certificate is valid', 'certificate': cert}


