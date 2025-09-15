from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# database'e bağlanmak için kullanılır
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 