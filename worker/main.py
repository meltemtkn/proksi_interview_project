import sys
import os
import logging
import time
from typing import Optional

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../backend')
sys.path.insert(0, backend_path)

# Backend imports (backend. prefix olmadan)
from app.core.celery_app import celery_app
from app.db.session import get_db
from app.models.notes import Note, Status
from sqlalchemy.orm import Session

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_session() -> Session:
    # database session'ı alınır
    return next(get_db())


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60}, name='worker.summarize_note')
def summarize_note(self, note_id: str) -> Optional[str]:
    # note'ın id'si alınır
    logger.info(f"Starting summarization for note {note_id}")
    
    try:
        # database session'ı alınır
        db = get_db_session()
        
        # note'ın id'si alınır
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            logger.error(f"Note {note_id} not found")
            return None
        
        # status'u IN_PROGRESS'e güncellenir
        note.status = Status.IN_PROGRESS
        db.commit()
        logger.info(f"Updated note {note_id} status to IN_PROGRESS")
        
        # 5 saniye beklenir
        time.sleep(5)
        
        # rule-based summarization (stub)
        raw_text = note.raw_text
        summary = generate_summary(raw_text)
        
        # note'a summary eklenir
        note.summary = summary
        note.status = Status.COMPLETED
        db.commit()
        
        logger.info(f"Successfully summarized note {note_id}")
        return summary
        
    except Exception as exc:
        logger.error(f"Error summarizing note {note_id}: {str(exc)}")
        
        # status'u FAILED'e güncellenir
        try:
            db = get_db_session()
            note = db.query(Note).filter(Note.id == note_id).first()
            if note:
                note.status = Status.FAILED
                db.commit()
                logger.info(f"Updated note {note_id} status to FAILED")
        except Exception as db_exc:
            logger.error(f"Failed to update note status: {str(db_exc)}")
        
        # Celery retry mekanizması için yeniden fırlatılır
        raise self.retry(exc=exc)
    
    finally:
        # database session'ı kapatılır
        try:
            db.close()
        except:
            pass


def generate_summary(text: str) -> str:
    # simple rule-based text summarization
    # Basic rules for summarization
    sentences = text.split('.')
    
    # empty sentences kaldırılır
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # text kısa ise text döndürülür
    if len(sentences) <= 2:
        return text
    
    # simple extractive summarization - first and last sentences alınır
    if len(sentences) <= 5:
        summary = '. '.join(sentences[:2])
    else:
        # longer texts için first 2 and last 1 sentences alınır
        summary = '. '.join(sentences[:2] + [sentences[-1]])
    
    # text kısaltıldıysa ellipsis eklenir
    if len(summary) < len(text) * 0.7:
        summary += "..."
    
    return summary.strip() + "." if not summary.endswith('.') else summary.strip()


if __name__ == "__main__":
    print("Starting Celery worker...")
    print("Registered tasks:")
    print("   - worker.summarize_note")
    print("")
    
    # worker'ı başlatır
    import __main__
    
    # worker'ı başlatır
    celery_app.worker_main(['worker', '--loglevel=info', '--concurrency=1'])
