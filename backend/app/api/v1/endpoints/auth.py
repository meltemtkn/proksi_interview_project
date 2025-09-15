from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.crud.users_crud import authenticate_user, create_user, get_user_by_email
from app.schemas.users import UserCreate, UserResponse

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create new user account"""
    # Check if user already exists
    existing_user = get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    user = create_user(db, user_in=user_in)
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
