# Use multi-stage build to reduce attack surface
FROM python:3.11-alpine AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-alpine

# Add security labels
LABEL org.opencontainers.image.vendor="Your Organization"
LABEL org.opencontainers.image.title="Markdown to EPUB Converter"
LABEL org.opencontainers.image.description="Secure container for converting markdown to EPUB"

# Install runtime dependencies only
RUN apk add --no-cache pandoc && \
    # Add security updates
    apk upgrade --no-cache && \
    # Clean up
    rm -rf /var/cache/apk/* && \
    # Create non-root user
    addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    # Create app directory with proper permissions
    mkdir -p /app /app/tmp && \
    chown -R appuser:appgroup /app

# Set working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY --chown=appuser:appgroup app.py .

# Set secure environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    GUNICORN_CMD_ARGS="--log-level=debug"

# Set temporary directory for the application
ENV TMPDIR=/app/tmp

# Expose port
EXPOSE 5000

# Add debugging tools
RUN apk add --no-cache curl wget procps htop

# Switch to non-root user
USER appuser

# Set health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1

# Set resource limits
# Note: These are set at runtime, but documented here
# --memory="512m" --memory-swap="1g" --cpus="1.0"

# Run the application with gunicorn with enhanced logging
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "--keep-alive", "2", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "--capture-output", "--enable-stdio-inheritance", "app:app"]
