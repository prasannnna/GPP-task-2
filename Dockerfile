# ============================
# Stage 1: Builder
# ============================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies into /deps
RUN pip install --prefix=/deps -r requirements.txt


# ============================
# Stage 2: Runtime
# ============================
FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

# Install system packages for cron
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /deps /usr/local

# Copy application code
COPY app ./app
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Copy cron job file
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Correct cron file permissions
RUN chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron

# Create volumes
RUN mkdir -p /data && \
    mkdir -p /cron && \
    chmod 755 /data /cron

EXPOSE 8080

# Start cron + FastAPI
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8080
