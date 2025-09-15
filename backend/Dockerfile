FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Proksi Interview Project API..."\n\
echo "Waiting for database..."\n\
while ! pg_isready -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-user} -d ${POSTGRES_DB:-proksi_db} > /dev/null 2>&1; do\n\
    sleep 2\n\
done\n\
echo "Database is ready!"\n\
echo "Running database migrations..."\n\
alembic upgrade head\n\
echo "Starting API server..."\n\
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}' > /app/start.sh

RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Command to run the startup script
CMD ["/app/start.sh"]
