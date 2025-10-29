from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from database import get_db
from models import User, Notification, Book
from schemas import NotificationResponse
from auth_utils import get_current_active_user
from config import settings

router = APIRouter()

# Email notification function
async def send_email_notification(to_email: str, subject: str, body: str):
    """Send email notification."""
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SMTP_USERNAME, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
# Notification endpoints
@router.get("/", response_model=List[NotificationResponse])
async def get_user_notifications(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's notifications."""
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()
    
    return notifications

@router.post("/mark-read/{notification_id}")
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification.is_sent = True
    notification.sent_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Notification marked as read"}

@router.post("/subscribe/new-releases")
async def subscribe_to_new_releases(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Subscribe user to new release notifications."""
    # Update user preferences
    current_user.email_notifications = True
    db.commit()
    
    return {"message": "Successfully subscribed to new release notifications"}

@router.post("/unsubscribe/new-releases")
async def unsubscribe_from_new_releases(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Unsubscribe user from new release notifications."""
    # Update user preferences
    current_user.email_notifications = False
    db.commit()
    
    return {"message": "Successfully unsubscribed from new release notifications"}

# Background task to send notifications
async def send_new_release_notifications(book_id: int, db: Session):
    """Send notifications about new book releases."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return
    
    # Get users who want email notifications
    users = db.query(User).filter(User.email_notifications == True).all()
    
    for user in users:
        # Create notification record
        notification = Notification(
            user_id=user.id,
            title="New Book Release!",
            message=f"'{book.title}' by {book.author} is now available in our library!",
            notification_type="email"
        )
        db.add(notification)
        
        # Send email
        subject = "New Book Release - EaseOps E-Library"
        body = f"""
        <html>
        <body>
            <h2>New Book Release!</h2>
            <p>Hello {user.full_name or user.username},</p>
            <p>We're excited to announce that <strong>"{book.title}"</strong> by {book.author} is now available in our library!</p>
            <p>Click <a href="https://easeops-elibrary.com/books/{book.id}">here</a> to read it now.</p>
            <p>Happy reading!</p>
            <p>EaseOps E-Library Team</p>
        </body>
        </html>
        """
        
        email_sent = await send_email_notification(user.email, subject, body)
        if email_sent:
            notification.is_sent = True
            notification.sent_at = datetime.utcnow()
    
    db.commit()

# Admin endpoint to trigger new release notifications
@router.post("/trigger/new-release/{book_id}")
async def trigger_new_release_notification(
    book_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger new release notifications for a book."""
    background_tasks.add_task(send_new_release_notifications, book_id, db)
    return {"message": "New release notifications queued"}

# Replace the entire test endpoint with:
@router.post("/test")
async def send_test_notification(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Send a test email notification to the current user."""
    if not current_user.email_notifications:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email notifications are disabled for this user"
        )
    
    subject = "Test Notification - EaseOps E-Library"
    body = f"""
    <html>
    <body>
        <h2>Test Notification</h2>
        <p>Hello {current_user.full_name or current_user.username},</p>
        <p>This is a test notification to verify your email settings.</p>
        <p>If you received this email, your notification settings are working correctly!</p>
        <p>EaseOps E-Library Team</p>
    </body>
    </html>
    """
    
    email_sent = await send_email_notification(current_user.email, subject, body)
    
    if email_sent:
        return {"message": "Test email notification sent successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send test email notification"
        )