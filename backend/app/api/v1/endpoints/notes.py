from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.notes import Note

router = APIRouter()

@router.get("/")
async def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()