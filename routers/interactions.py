from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, Feedback, ContactRequest, Survey, SurveyResponse, Book
from schemas import FeedbackCreate, FeedbackResponse, ContactRequestCreate, ContactRequestResponse, SurveyResponseCreate
from auth_utils import get_current_active_user

router = APIRouter()

# Feedback endpoints
@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    feedback: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit feedback."""
    db_feedback = Feedback(
        user_id=current_user.id,
        feedback_type=feedback.feedback_type,
        subject=feedback.subject,
        message=feedback.message
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return db_feedback

@router.get("/feedback", response_model=List[FeedbackResponse])
async def get_user_feedback(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's feedback submissions."""
    feedback = db.query(Feedback).filter(Feedback.user_id == current_user.id).order_by(Feedback.created_at.desc()).all()
    return feedback

# Contact request endpoints
@router.post("/contact", response_model=ContactRequestResponse)
async def submit_contact_request(
    contact: ContactRequestCreate,
    db: Session = Depends(get_db)
):
    """Submit a contact request."""
    db_contact = ContactRequest(
        name=contact.name,
        email=contact.email,
        subject=contact.subject,
        message=contact.message
    )
    
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    return db_contact

# Survey endpoints
@router.get("/surveys")
async def get_active_surveys(db: Session = Depends(get_db)):
    """Get active surveys."""
    surveys = db.query(Survey).filter(Survey.is_active == True).all()
    return surveys

@router.get("/surveys/{survey_id}")
async def get_survey(survey_id: int, db: Session = Depends(get_db)):
    """Get a specific survey."""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey not found"
        )
    return survey

@router.post("/surveys/{survey_id}/respond")
async def respond_to_survey(
    survey_id: int,
    response: SurveyResponseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit a survey response."""
    # Check if survey exists and is active
    survey = db.query(Survey).filter(
        Survey.id == survey_id,
        Survey.is_active == True
    ).first()
    
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey not found or inactive"
        )
    
    # Check if user already responded
    existing_response = db.query(SurveyResponse).filter(
        SurveyResponse.survey_id == survey_id,
        SurveyResponse.user_id == current_user.id
    ).first()
    
    if existing_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has already responded to this survey"
        )
    
    # Create response
    db_response = SurveyResponse(
        survey_id=survey_id,
        user_id=current_user.id,
        responses=str(response.responses)  # Convert dict to string for storage
    )
    
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    return {"message": "Survey response submitted successfully"}

# FAQ endpoint (simplified)
@router.get("/faq")
async def get_faq():
    """Get frequently asked questions."""
    faq_data = [
        {
            "question": "How do I bookmark a book?",
            "answer": "Click the bookmark icon on any book page to add it to your bookmarks."
        },
        {
            "question": "Can I read books offline?",
            "answer": "Yes, you can download books for offline reading. Look for the download option on the book page."
        },
        {
            "question": "How do I change my reading preferences?",
            "answer": "Go to your profile settings to update your reading preferences including dark mode."
        },
        {
            "question": "How do I contact support?",
            "answer": "Use the contact form or submit feedback through the app to reach our support team."
        }
    ]
    return faq_data

# Social sharing endpoint (simplified)
@router.post("/share/{book_id}")
async def share_book(
    book_id: int,
    share_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Share a book on social media."""
    # Check if book exists
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Generate share URL (simplified)
    share_url = f"https://easeops-elibrary.com/books/{book_id}"
    share_text = f"Check out '{book.title}' by {book.author} on EaseOps E-Library!"
    
    return {
        "message": "Book shared successfully",
        "share_url": share_url,
        "share_text": share_text,
        "platform": share_data.get("platform", "unknown")
    }