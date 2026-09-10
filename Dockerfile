# Explicit base image version (never use `latest`)
FROM python:3.11-slim

# Metadata labels (Part 23 - overridden/extended at build time via --build-arg + ARG below)
ARG APP_VERSION=unknown
ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.source="https://github.com/<your-username>/student-ml-api"

WORKDIR /app

# Install dependencies first (better layer caching -- see Part 25)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code after dependencies so code changes
# don't invalidate the dependency-install layer
COPY app.py .
COPY VERSION .

EXPOSE 5000

CMD ["python", "app.py"]
