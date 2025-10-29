from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserProfile
from schemas import UserUpdate, UserResponse
from auth_utils import get_current_active_user

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user's profile."""
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user profile and preferences."""
    # Update user fields
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.dark_mode is not None:
        current_user.dark_mode = user_update.dark_mode
    if user_update.email_notifications is not None:
        current_user.email_notifications = user_update.email_notifications
    if user_update.whatsapp_notifications is not None:
        current_user.whatsapp_notifications = user_update.whatsapp_notifications
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/preferences")
async def get_user_preferences(current_user: User = Depends(get_current_active_user)):
    """Get user preferences."""
    return {
        "dark_mode": current_user.dark_mode,
        "email_notifications": current_user.email_notifications,
        "whatsapp_notifications": current_user.whatsapp_notifications
    }

@router.put("/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user preferences."""
    if "dark_mode" in preferences:
        current_user.dark_mode = preferences["dark_mode"]
    if "email_notifications" in preferences:
        current_user.email_notifications = preferences["email_notifications"]
    if "whatsapp_notifications" in preferences:
        current_user.whatsapp_notifications = preferences["whatsapp_notifications"]
    
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Preferences updated successfully"}
