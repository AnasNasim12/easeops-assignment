from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from database import get_db
from models import Book, User
from schemas import BookResponse, BookCreate
from auth_utils import get_current_active_user

router = APIRouter()

@router.get("/books", response_model=List[BookResponse])
async def get_books(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title, author, or description"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get list of books with optional filtering."""
    query = db.query(Book).filter(Book.is_available == True)
    
    # Filter by category
    if category:
        query = query.filter(Book.category == category)
    
    # Search functionality
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_term),
                Book.author.ilike(search_term),
                Book.description.ilike(search_term)
            )
        )
    
    # Filter by tags (simplified - in production, you'd want proper tag handling)
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        for tag in tag_list:
            query = query.filter(Book.tags.ilike(f"%{tag}%"))
    
    books = query.offset(skip).limit(limit).all()
    return books

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get list of all book categories."""
    categories = db.query(Book.category).distinct().all()
    return [category[0] for category in categories]

@router.get("/tags")
async def get_tags(db: Session = Depends(get_db)):
    """Get list of all book tags."""
    # This is a simplified implementation - in production, you'd want proper tag normalization
    books = db.query(Book.tags).filter(Book.tags.isnot(None)).all()
    all_tags = set()
    for book_tags in books:
        if book_tags[0]:
            # Assuming tags are stored as comma-separated string
            tags = [tag.strip() for tag in book_tags[0].split(",")]
            all_tags.update(tags)
    
    return list(all_tags)

@router.get("/featured")
async def get_featured_books(
    limit: int = Query(5, ge=1, le=20, description="Number of featured books to return"),
    db: Session = Depends(get_db)
):
    """Get featured books (newest books)."""
    books = db.query(Book).filter(Book.is_available == True).order_by(Book.created_at.desc()).limit(limit).all()
    return books

@router.get("/popular")
async def get_popular_books(
    limit: int = Query(5, ge=1, le=20, description="Number of popular books to return"),
    db: Session = Depends(get_db)
):
    """Get popular books (most bookmarked)."""
    # This is a simplified implementation - in production, you'd track views/downloads
    books = db.query(Book).filter(Book.is_available == True).limit(limit).all()
    return books
