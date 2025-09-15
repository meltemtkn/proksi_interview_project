from celery import Celery
from app.core.settings import settings

celery_app = Celery(
    "proksi_worker", # celery worker'ın çalıştığı uygulama adı
    broker=settings.CELERY_BROKER_URL, # celery worker'ın broker'ının adresi
    backend=settings.CELERY_RESULT_BACKEND, # celery worker'ın backend'inin adresi
)

# Configuration - celery worker'ın çalışması için gerekli olan ayarlar
celery_app.conf.update(
    task_serializer="json", # task'ın gönderilmesi için kullanılacak serializer
    accept_content=["json"], # celery worker'ın kabul edeceği content tipleri
    result_serializer="json", # task'ın sonucunun gönderilmesi için kullanılacak serializer
    timezone="UTC", # timezone ayarları
    enable_utc=True, # UTC timezone'ını kullan
    result_expires=3600, # task'ın sonucunun ne kadar süre sonra silineceği
    task_track_started=True, # task'ın başladığını takip et
    task_retry_jitter=True, # task'ın yeniden denenmesi için jitter ayarları
    task_retry_max_delay=600, # task'ın yeniden denenmesi için maksimum delay
    task_soft_time_limit=300, # task'ın soft time limit'i
    task_time_limit=600, # task'ın time limit'i
) 