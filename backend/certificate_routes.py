"""
Certificate System Backend Routes
- Progress tracking by age group
- Certificate generation with QR codes
- Admin approval workflow
- Public verification
"""

from fastapi import HTTPException, Depends
from typing import Optional
import qrcode
import io
import base64
from datetime import datetime, timezone

# Add these routes to server.py

@api_router.get("/certificates/progress")
async def get_certificate_progress(current_user: dict = Depends(get_current_user)):
    """Get user's certificate progress by age group"""
    user_id = current_user['sub']
    
    # Count completed lessons per age group
    age_groups = ['5-7', '8-9', '10-12', '13-15', '16-18']
    progress = []
    
    for age_group in age_groups:
        total_lessons = await lessons_collection.count_documents({
            'is_ai_curriculum': True,
            'age_group': age_group
        })
        
        # Count user's completed lessons
        completed = await progress_collection.count_documents({
            'user_id': user_id,
            'age_group': age_group,
            'completed': True
        })
        
        # Check if certificate exists
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
            'unlocked': completed >= (total_lessons * 0.8)  # 80% completion to unlock
        })
    
    return {'progress': progress}


@api_router.post("/certificates/request")
async def request_certificate(
    age_group: str,
    current_user: dict = Depends(get_current_user)
):
    """Request a certificate for completed age group"""
    user_id = current_user['sub']
    
    # Check if user has completed enough lessons
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
            detail=f"Complete at least 80% of lessons to request certificate ({completed}/{total_lessons})"
        )
    
    # Check if certificate already exists
    existing = await certificates_collection.find_one({
        'user_id': user_id,
        'age_group': age_group
    })
    
    if existing:
        return {'message': 'Certificate already exists', 'certificate_number': existing['certificate_number']}
    
    # Generate certificate number (format: CERT-YYYY-XXXXXX)
    count = await certificates_collection.count_documents({})
    cert_number = f"CERT-{datetime.now().year}-{str(count + 1).zfill(6)}"
    
    # Get user info
    user_doc = await users_collection.find_one({'id': user_id})
    
    # Create certificate request
    certificate = {
        'id': str(__import__('uuid').uuid4()),
        'certificate_number': cert_number,
        'user_id': user_id,
        'student_name': user_doc.get('name', 'Student'),
        'age_group': age_group,
        'program': 'AI & STEAM Education',
        'total_lessons': total_lessons,
        'completed_lessons': completed,
        'status': 'approved',  # Auto-approve for now
        'requested_date': datetime.now(timezone.utc).isoformat(),
        'approved_date': datetime.now(timezone.utc).isoformat(),
        'approved_by': 'system'
    }
    
    await certificates_collection.insert_one(certificate)
    
    return {
        'message': 'Certificate approved!',
        'certificate_number': cert_number
    }


@api_router.get("/certificates/{cert_number}")
async def get_certificate(cert_number: str):
    """Get certificate details for display/printing"""
    cert = await certificates_collection.find_one(
        {'certificate_number': cert_number},
        {'_id': 0}
    )
    
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    # Generate QR code for verification
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
    """Public verification endpoint - no auth required"""
    cert = await certificates_collection.find_one(
        {'certificate_number': cert_number},
        {'_id': 0, 'id': 0, 'user_id': 0}
    )
    
    if not cert:
        return {
            'valid': False,
            'message': 'Certificate not found'
        }
    
    if cert['status'] != 'approved':
        return {
            'valid': False,
            'message': 'Certificate not approved',
            'certificate': cert
        }
    
    return {
        'valid': True,
        'message': 'Certificate is valid and verified',
        'certificate': cert
    }


# Admin endpoints
@api_router.get("/admin/certificates/pending", dependencies=[Depends(require_admin)])
async def get_pending_certificates():
    """Get all pending certificate requests"""
    certs = await certificates_collection.find(
        {'status': 'pending'},
        {'_id': 0}
    ).to_list(length=100)
    
    return {'certificates': certs}


@api_router.post("/admin/certificates/{cert_id}/approve", dependencies=[Depends(require_admin)])
async def approve_certificate(cert_id: str, current_user: dict = Depends(get_current_user)):
    """Approve a certificate request"""
    result = await certificates_collection.update_one(
        {'id': cert_id},
        {'$set': {
            'status': 'approved',
            'approved_date': datetime.now(timezone.utc).isoformat(),
            'approved_by': current_user['sub']
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    return {'message': 'Certificate approved'}
