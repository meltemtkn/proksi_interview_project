from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.notes import Note, Status
from app.schemas.notes import NoteCreate, NoteResponse
from app.core.security import get_current_user, get_current_admin_user
from app.schemas.users import Role, User
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("/", response_model=NoteResponse)
async def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    # Create note with QUEUED status
    db_note = Note(
        raw_text=note_in.raw_text,
        summary="",  # Will be filled by background job
        status=Status.QUEUED,
        user_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    # Queue background job for AI summarization
    try:
        celery_app.send_task('worker.summarize_note', args=[db_note.id])
        print(f"Task queued for note {db_note.id}")
    except Exception as e:
        # If we can't queue the job, mark as FAILED
        print(f"Failed to queue summarization job: {e}")
        db_note.status = Status.FAILED
        db.commit()
        print(f"Updated note {db_note.id} status to FAILED")
    
    return db_note


@router.get("/", response_model=List[NoteResponse])
async def get_notes(
    db: Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    if current_user.role == Role.ADMIN:
        # Admins can see all notes
        notes = db.query(Note).all()
    else:
        # Agents and others can only see their own notes
        notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Check permissions - agents can only see their own notes
    if current_user.role != Role.ADMIN and note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this note"
        )
    
    return note


@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    if current_user.role != Role.ADMIN and note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this note"
        )
    
    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted successfully"}