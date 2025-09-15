import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the parent directory to Python path for local development
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import router
from app.core.settings import settings

def create_app() -> FastAPI:
    # app and router creation
    app = FastAPI(
        title="Proksi Interview Project API",
        description="A FastAPI application for managing users and notes",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add root endpoint
    @app.get("/")
    async def root():
        """Welcome endpoint with API information"""
        return {
            "message": "Welcome to Proksi Interview Project API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "endpoints": {
                "auth": "/api/auth",
                "notes": "/api/notes"
            }
        }
    
    app.include_router(router)
    
    # Initialize database - make it optional
    try:
        from app.db.session import get_db
        from app.db.init_db import init_db
        
        db = next(get_db())
        init_db(db)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
        print("Application will start without database initialization")
        print("Make sure PostgreSQL is running and accessible")

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True, workers=1)