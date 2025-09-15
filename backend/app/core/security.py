import os
import secrets
from datetime import datetime, timedelta
from typing import Any, Union, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.users import Role, User

# Security Configuration
ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')
SECRET_KEY: str = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))

# JWT Bearer Token
security = HTTPBearer()


def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]: # token'ın doğruluğunu kontrol et
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject: str = payload.get("sub")
        if subject is None:
            return None
        return subject
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    # get_user_by_email'i burada import etmek için gerekli
    from app.crud.users_crud import get_user_by_email
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user


def get_current_admin_user(current_user:User = Depends(get_current_user)):
    # admin rolü gerektirir
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_current_agent_or_admin_user(current_user:User = Depends(get_current_user)):
    # agent veya admin rolü gerektirir
    if current_user.role not in [Role.AGENT, Role.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user