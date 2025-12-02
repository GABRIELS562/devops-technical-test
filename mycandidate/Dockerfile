# MyCandidate Flask Application
# Multi-stage build for smaller, secure production image

# Stage 1: Builder
# We need gcc and dev libraries to compile some Python packages
# cryptography and psycopg2 may require compilation on some systems
FROM python:3.10-slim as builder

WORKDIR /build

# Install build dependencies
# libpq-dev: PostgreSQL client library headers (for psycopg2)
# libffi-dev: Foreign function interface (for cryptography)
# gcc: C compiler for packages with native extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker layer caching)
# If requirements.txt hasn't changed, this layer is cached
COPY requirements.txt .

# Install Python packages to a specific directory
# We'll copy only this directory to the production image
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Production
# Fresh slim image without build tools (smaller and more secure)
FROM python:3.10-slim as production

WORKDIR /app

# Install only runtime dependencies (no dev headers)
# libpq5: PostgreSQL client library (runtime only)
# curl: For health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
# This is where multi-stage saves space - we don't carry gcc, headers etc
COPY --from=builder /install /usr/local

# Create non-root user for security
# Running as root in containers is a security risk
RUN useradd --create-home --shell /bin/bash appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Flask default port
EXPOSE 5000

# Health check for container orchestration (Docker Swarm, ECS, etc)
# Checks if the app responds within 30 seconds
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run with gunicorn (matches Procfile)
# 4 workers is a good default (2 * CPU cores + 1)
# bind 0.0.0.0 so container is accessible from outside
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
