from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Book, UserNote, user_bookmarks
from schemas import BookResponse, UserNoteCreate, UserNoteResponse
from auth_utils import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[BookResponse])
async def get_user_bookmarks(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's bookmarked books."""
    bookmarks = db.query(Book).join(user_bookmarks).filter(
        user_bookmarks.c.user_id == current_user.id
    ).all()
    return bookmarks

@router.get("/notes", response_model=List[UserNoteResponse])
async def get_user_notes(
    book_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's notes, optionally filtered by book."""
    query = db.query(UserNote).filter(UserNote.user_id == current_user.id)
    
    if book_id:
        query = query.filter(UserNote.book_id == book_id)
    
    notes = query.order_by(UserNote.created_at.desc()).all()
    return notes

@router.post("/notes", response_model=UserNoteResponse)
async def create_note(
    note: UserNoteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new note for a book."""
    # Check if book exists
    book = db.query(Book).filter(Book.id == note.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Create note
    db_note = UserNote(
        user_id=current_user.id,
        book_id=note.book_id,
        page_number=note.page_number,
        note_text=note.note_text
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return db_note

@router.put("/notes/{note_id}", response_model=UserNoteResponse)
async def update_note(
    note_id: int,
    note_text: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a user's note."""
    note = db.query(UserNote).filter(
        UserNote.id == note_id,
        UserNote.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    note.note_text = note_text
    db.commit()
    db.refresh(note)
    
    return note

@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a user's note."""
    note = db.query(UserNote).filter(
        UserNote.id == note_id,
        UserNote.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted successfully"}

@router.post("/{book_id}")
async def add_bookmark(
    book_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a book to user's bookmarks."""
    # Check if book exists
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check if already bookmarked
    existing_bookmark = db.query(user_bookmarks).filter(
        user_bookmarks.c.user_id == current_user.id,
        user_bookmarks.c.book_id == book_id
    ).first()
    
    if existing_bookmark:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book already bookmarked"
        )
    
    # Add bookmark
    db.execute(
        user_bookmarks.insert().values(
            user_id=current_user.id,
            book_id=book_id
        )
    )
    db.commit()
    
    return {"message": "Book bookmarked successfully"}

@router.delete("/{book_id}")
async def remove_bookmark(
    book_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a book from user's bookmarks."""
    # Check if bookmark exists
    existing_bookmark = db.query(user_bookmarks).filter(
        user_bookmarks.c.user_id == current_user.id,
        user_bookmarks.c.book_id == book_id
    ).first()
    
    if not existing_bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    # Remove bookmark
    db.execute(
        user_bookmarks.delete().where(
            user_bookmarks.c.user_id == current_user.id,
            user_bookmarks.c.book_id == book_id
        )
    )
    db.commit()
    
    return {"message": "Bookmark removed successfully"}