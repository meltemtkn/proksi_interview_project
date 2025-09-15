from sqlalchemy.orm import Session

from app.crud.users_crud import get_user_by_email, create_user
from app.core.settings import settings
from app.schemas.users import UserCreate, Role


def init_db(db: Session) -> None:
    # Note: Tables should be created via Alembic migrations
    # This function only creates the initial admin user
    # Create admin user if it doesn't exist
    admin_user = get_user_by_email(db, email=settings.FIRST_SUPERUSER) # admin kullanıcısı var mı kontrol ediliyor
    if not admin_user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            role=Role.ADMIN
        )
        admin_user = create_user(db, user_in=user_in)
        print(f"Admin user created: {admin_user.email}")
    else:
        print(f"Admin user already exists: {admin_user.email}")
        
    print("Database initialization completed.")





