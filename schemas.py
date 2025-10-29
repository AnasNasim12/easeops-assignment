from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Union
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    dark_mode: Optional[bool] = None
    email_notifications: Optional[bool] = None
    whatsapp_notifications: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    dark_mode: bool
    email_notifications: bool
    whatsapp_notifications: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Book schemas
class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    category: str
    tags: Optional[Union[List[str], str]] = None
    cover_image_url: Optional[str] = None
    language: str = "English"

class BookCreate(BookBase):
    isbn: Optional[str] = None
    book_file_url: Optional[str] = None
    file_size: Optional[int] = None
    page_count: Optional[int] = None
    published_date: Optional[datetime] = None

class BookResponse(BookBase):
    id: int
    isbn: Optional[str]
    file_size: Optional[int]
    page_count: Optional[int]
    published_date: Optional[datetime]
    is_available: bool
    created_at: datetime
    
    @validator('tags', pre=True)
    def parse_tags(cls, v):
        if isinstance(v, str):
            try:
                import json
                return json.loads(v)
            except:
                return []
        return v or []
    
    class Config:
        from_attributes = True
# User Note schemas
class UserNoteBase(BaseModel):
    book_id: int
    page_number: Optional[int] = None
    note_text: str

class UserNoteCreate(UserNoteBase):
    pass

class UserNoteResponse(UserNoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Feedback schemas
class FeedbackBase(BaseModel):
    feedback_type: str
    subject: str
    message: str

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    user_id: Optional[int]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Contact Request schemas
class ContactRequestBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactRequestCreate(ContactRequestBase):
    pass

class ContactRequestResponse(ContactRequestBase):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Survey schemas
class SurveyResponse(BaseModel):
    survey_id: int
    responses: dict

class SurveyResponseCreate(SurveyResponse):
    pass

# Notification schemas
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    notification_type: str
    is_sent: bool
    sent_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
