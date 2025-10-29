import asyncio
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, Book, Survey
from auth_utils import get_password_hash
import json

def create_sample_data():
    """Create sample data for testing the API."""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create sample users
        users_data = [
            {
                "email": "john.doe@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "password123",
                "dark_mode": False,
                "email_notifications": True
            },
            {
                "email": "jane.smith@example.com",
                "username": "janesmith",
                "full_name": "Jane Smith",
                "password": "password123",
                "dark_mode": True,
                "email_notifications": True
            },
            {
                "email": "admin@easeops.com",
                "username": "admin",
                "full_name": "Admin User",
                "password": "admin123",
                "dark_mode": False,
                "email_notifications": True
            }
        ]
        
        for user_data in users_data:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    email=user_data["email"],
                    username=user_data["username"],
                    full_name=user_data["full_name"],
                    hashed_password=get_password_hash(user_data["password"]),
                    dark_mode=user_data["dark_mode"],
                    email_notifications=user_data["email_notifications"],
                    is_verified=True
                )
                db.add(user)
        
        # Create sample books
        books_data = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A classic American novel set in the Jazz Age.",
                "category": "Fiction",
                "tags": ["classic", "american", "literature"],
                "isbn": "9780743273565",
                "language": "English",
                "page_count": 180
            },
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "description": "A gripping tale of racial injustice and childhood innocence.",
                "category": "Fiction",
                "tags": ["classic", "american", "drama"],
                "isbn": "9780061120084",
                "language": "English",
                "page_count": 281
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "description": "A dystopian social science fiction novel.",
                "category": "Science Fiction",
                "tags": ["dystopian", "political", "classic"],
                "isbn": "9780451524935",
                "language": "English",
                "page_count": 328
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "description": "A romantic novel of manners.",
                "category": "Romance",
                "tags": ["classic", "romance", "english"],
                "isbn": "9780141439518",
                "language": "English",
                "page_count": 432
            },
            {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "description": "A coming-of-age story about teenage rebellion.",
                "category": "Fiction",
                "tags": ["coming-of-age", "american", "classic"],
                "isbn": "9780316769174",
                "language": "English",
                "page_count": 277
            },
            {
                "title": "Python Programming",
                "author": "Mark Lutz",
                "description": "Comprehensive guide to Python programming language.",
                "category": "Programming",
                "tags": ["programming", "python", "technical"],
                "isbn": "9781449355739",
                "language": "English",
                "page_count": 1648
            },
            {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "description": "A handbook of agile software craftsmanship.",
                "category": "Programming",
                "tags": ["programming", "software", "best-practices"],
                "isbn": "9780132350884",
                "language": "English",
                "page_count": 464
            },
            {
                "title": "The Art of War",
                "author": "Sun Tzu",
                "description": "Ancient Chinese military treatise.",
                "category": "Philosophy",
                "tags": ["philosophy", "strategy", "ancient"],
                "isbn": "9781590309637",
                "language": "English",
                "page_count": 273
            }
        ]
        
        for book_data in books_data:
            existing_book = db.query(Book).filter(Book.title == book_data["title"]).first()
            if not existing_book:
                book = Book(
                    title=book_data["title"],
                    author=book_data["author"],
                    description=book_data["description"],
                    category=book_data["category"],
                    tags=json.dumps(book_data["tags"]),
                    isbn=book_data["isbn"],
                    language=book_data["language"],
                    page_count=book_data["page_count"],
                    is_available=True
                )
                db.add(book)
        
        # Create sample survey
        survey_data = {
            "title": "EaseOps E-Library User Experience Survey",
            "description": "Help us improve your reading experience",
            "questions": json.dumps([
                {
                    "id": 1,
                    "question": "How often do you use the EaseOps E-Library?",
                    "type": "multiple_choice",
                    "options": ["Daily", "Weekly", "Monthly", "Rarely"]
                },
                {
                    "id": 2,
                    "question": "What features do you find most useful?",
                    "type": "multiple_select",
                    "options": ["Bookmarks", "Notes", "Search", "Categories", "Notifications"]
                },
                {
                    "id": 3,
                    "question": "Rate your overall experience (1-5)",
                    "type": "rating",
                    "min": 1,
                    "max": 5
                },
                {
                    "id": 4,
                    "question": "Any suggestions for improvement?",
                    "type": "text"
                }
            ]),
            "is_active": True
        }
        
        existing_survey = db.query(Survey).filter(Survey.title == survey_data["title"]).first()
        if not existing_survey:
            survey = Survey(
                title=survey_data["title"],
                description=survey_data["description"],
                questions=survey_data["questions"],
                is_active=survey_data["is_active"]
            )
            db.add(survey)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
