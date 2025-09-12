from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    notes
)

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(notes.router, prefix="/notes", tags=["notes"])