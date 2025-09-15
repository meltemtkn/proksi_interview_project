# Proksi Interview Project

Bu bir **note-taking app** backend'i:
- Kullanıcılar signup/login olabiliyor (JWT ile)
- Notlar oluşturabiliyor 
- Robot otomatik not özetliyor (background'da)
- Admin tüm notları görebiliyor, normal kullanıcılar sadece kendi notlarını

## Teknolojiler

**Backend:**
- **FastAPI** - API framework 
- **PostgreSQL** - Database (verileri saklar)
- **Redis** - Message queue (job'ları sıraya koyar)
- **Celery** - Background jobs (arka planda iş yapar)
- **Docker** - Containerization (her yerde aynı çalışır)

## Nasıl Çalıştırırım?

### 1. Kolay Yol - Docker Compose
```bash
git clone <repo-url>
cd proksi_interview_project
docker-compose up --build
```

### 2. Manuel Kurulum
```bash
# PostgreSQL ve Redis başlat
docker-compose up postgres redis -d

# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head  # Database tablolarını oluştur
uvicorn main:app --reload

# Worker (ayrı terminal)
cd worker  
pip install -r requirements.txt
celery -A backend.app.core.celery_app worker --loglevel=info
```

## Nasıl Test Ederim?

API çalışınca şu adrese git: `http://localhost:8000/docs`

### 1. Kullanıcı Oluştur:
```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "123456", "role": "agent"}'
```

### 2. Login Ol:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@test.com&password=123456"
```

Token alacaksın, bunu not et!

### 3. Not Oluştur:
```bash
curl -X POST "http://localhost:8000/api/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"raw_text": "Bu uzun bir not. AI özetleyecek."}'
```

### 4. Notlarını Gör:
```bash
curl -X GET "http://localhost:8000/api/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Background Job Nasıl Çalışıyor?

1. **Not oluşturursan** → Status: `QUEUED` 
2. **Celery worker alır** → Status: `IN_PROGRESS`
3. **AI özetler (5 saniye)** → Status: `COMPLETED`
4. **Eğer hata olursa** → Status: `FAILED`

## Roller

- **ADMIN**: Herkesin notlarını görebilir
- **AGENT**: Sadece kendi notlarını görebilir

## Canlı Demo

**API URL**: `https://proksi-interview-project.onrender.com`  
**API Docs**: `https://proksi-interview-project.onrender.com/docs`

Test için:
- Admin: `admin@example.com` / `admin123`
- Yeni user oluşturabilirsin

## Dosya Yapısı

```
proksi_interview_project/
├── backend/           # FastAPI uygulaması
│   ├── app/
│   │   ├── api/       # Endpoint'ler (/auth, /notes)
│   │   ├── core/      # Ayarlar, güvenlik, celery
│   │   ├── models/    # Database modelleri
│   │   └── schemas/   # Request/Response modelleri
│   └── Dockerfile
├── worker/            # Background job worker
│   ├── main.py        # Celery worker
│   └── Dockerfile
├── docker-compose.yml # Tüm servisleri başlatır
└── README.md
```

## Environment Variables

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=proksi_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Auth
SECRET_KEY=your-secret-key
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin123
```

**"Database connection failed"** → PostgreSQL çalışıyor mu?
```bash
docker-compose up postgres -d
```

**"Redis connection failed"** → Redis çalışıyor mu?
```bash
docker-compose up redis -d
```

**"Worker not processing jobs"** → Celery worker çalışıyor mu?
```bash
celery -A backend.app.core.celery_app worker --loglevel=info
```
