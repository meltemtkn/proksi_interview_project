# Proksi Interview Project

A FastAPI-based REST API with JWT authentication, role-based access control, and background AI summarization using Celery.

## Features

- 🔐 **JWT Authentication** - Email/password signup and login
- 👥 **Role-based Access Control** - ADMIN and AGENT roles with proper tenancy
- 📝 **Notes Management** - CRUD operations for notes with user isolation
- 🤖 **AI Summarization** - Background job processing for note summarization
- 🐳 **Docker Support** - Complete containerized deployment
- 📊 **Database Migrations** - Alembic-powered SQL migrations
- 🔄 **Background Jobs** - Celery with Redis for async task processing

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Authentication**: JWT with bcrypt password hashing
- **Background Jobs**: Celery with Redis
- **Database**: PostgreSQL with Alembic migrations
- **Containerization**: Docker & Docker Compose

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone and run**:
   ```bash
   git clone <your-repo-url>
   cd proksi_interview_project
   docker-compose up --build
   ```

2. **The API will be available at**: `http://localhost:8000`

3. **API Documentation**: `http://localhost:8000/docs`

### Manual Setup

1. **Database Setup**:
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up postgres redis -d
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Run migrations
   alembic upgrade head
   
   # Start server
   uvicorn main:app --reload
   ```

3. **Worker Setup**:
   ```bash
   cd worker
   pip install -r requirements.txt
   
   # Start worker
   celery -A backend.app.core.celery_app worker --loglevel=info
   ```

## API Usage

### Authentication

1. **Signup** (Creates AGENT by default):
   ```bash
   curl -X POST "http://localhost:8000/api/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123", "role": "agent"}'
   ```

2. **Login**:
   ```bash
   curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=password123"
   ```

### Notes

1. **Create Note** (triggers AI summarization):
   ```bash
   curl -X POST "http://localhost:8000/api/notes/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"raw_text": "This is a long note that needs summarization. It contains multiple sentences and important information."}'
   ```

2. **Get Notes**:
   ```bash
   curl -X GET "http://localhost:8000/api/notes/" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

3. **Get Specific Note**:
   ```bash
   curl -X GET "http://localhost:8000/api/notes/{note_id}" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

4. **Health Check**:
   ```bash
   curl -X GET "http://localhost:8000/health"
   ```

## Role-based Access

- **ADMIN**: Can see all notes from all users
- **AGENT**: Can only see their own notes
- **Tenancy**: Automatically enforced - agents cannot access other users' data

## Background AI Summarization

When a note is created:
1. Status starts as `QUEUED`
2. Background worker picks up the task
3. Status changes to `IN_PROGRESS`
4. AI summarization runs (currently rule-based, can be replaced with actual AI)
5. Status changes to `COMPLETED` with summary, or `FAILED` if error occurs

## Environment Variables

```env
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
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Admin User
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin123
```

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `password_hash` (String)
- `role` (Enum: ADMIN, AGENT, WORKER)
- `created_at`, `updated_at` (Timestamps)

### Notes Table
- `id` (UUID, Primary Key)
- `raw_text` (String)
- `summary` (String)
- `status` (Enum: QUEUED, IN_PROGRESS, COMPLETED, FAILED)
- `user_id` (Foreign Key to Users)
- `created_at`, `updated_at` (Timestamps)

## Development

### Running Tests
```bash
# TODO: Add tests
pytest
```

### Adding Migrations
```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Monitoring Background Jobs
```bash
# Check worker status
celery -A backend.app.core.celery_app inspect active

# Monitor tasks
celery -A backend.app.core.celery_app flower
```

## Deployment

The application is ready for deployment to services like:
- **Koyeb** (with Hobby plan)
- **Railway**
- **Heroku**
- **AWS ECS/Fargate**

### Quick Deployment to Koyeb

1. **Create a Koyeb account** and install the CLI
2. **Set up services**:
   ```bash
   # Deploy to Koyeb
   koyeb service create proksi-backend \
     --git-url https://github.com/YOUR_USERNAME/proksi_interview_project \
     --git-branch main \
     --build-directory backend \
     --ports 8000:http \
     --env POSTGRES_HOST=YOUR_DB_HOST \
     --env POSTGRES_USER=YOUR_DB_USER \
     --env POSTGRES_PASSWORD=YOUR_DB_PASSWORD \
     --env POSTGRES_DB=YOUR_DB_NAME \
     --env REDIS_HOST=YOUR_REDIS_HOST \
     --env SECRET_KEY=your-production-secret \
     --env FIRST_SUPERUSER=admin@yourcompany.com \
     --env FIRST_SUPERUSER_PASSWORD=secure-admin-password

   koyeb service create proksi-worker \
     --git-url https://github.com/YOUR_USERNAME/proksi_interview_project \
     --git-branch main \
     --dockerfile worker/Dockerfile \
     --env POSTGRES_HOST=YOUR_DB_HOST \
     --env POSTGRES_USER=YOUR_DB_USER \
     --env POSTGRES_PASSWORD=YOUR_DB_PASSWORD \
     --env POSTGRES_DB=YOUR_DB_NAME \
     --env REDIS_HOST=YOUR_REDIS_HOST
   ```

3. **Database**: Use Koyeb Postgres or Neon for free PostgreSQL
4. **Redis**: Use Upstash or Redis Cloud free tier

### Environment Variables for Production

```env
# Database (use your cloud DB credentials)
POSTGRES_HOST=your-db-host.com
POSTGRES_PORT=5432
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=proksi_db

# Redis (use your cloud Redis credentials)
REDIS_HOST=your-redis-host.com
REDIS_PORT=6379
REDIS_DB=0

# Auth (generate secure values for production)
SECRET_KEY=your-super-secure-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Admin User (change for production)
FIRST_SUPERUSER=admin@yourcompany.com
FIRST_SUPERUSER_PASSWORD=secure-admin-password
```

### Live Demo Instructions

Once deployed, you can demo the API:

1. **Access API docs**: `https://your-app.koyeb.app/docs`
2. **Create AGENT user**: Use `/api/auth/signup`
3. **Login and get token**: Use `/api/auth/login`
4. **Create note**: Use `/api/notes/` with Bearer token
5. **Check status**: Watch note status change from `QUEUED` → `IN_PROGRESS` → `COMPLETED`
6. **Demo tenancy**: Create ADMIN user, show they see all notes

## Design Decisions

1. **FastAPI**: Modern, fast, automatic API documentation
2. **SQLAlchemy**: Robust ORM with migration support
3. **JWT**: Stateless authentication suitable for microservices
4. **Celery + Redis**: Reliable background job processing with retries
5. **Docker**: Consistent deployment across environments
6. **Role-based tenancy**: Simple but effective access control

## TODO / Future Improvements

- [ ] Add proper test suite
- [ ] Implement actual AI summarization (OpenAI, etc.)
- [ ] Add API rate limiting
- [ ] Add logging and monitoring
- [ ] Add email notifications
- [ ] Implement pagination for notes list
- [ ] Add note search functionality