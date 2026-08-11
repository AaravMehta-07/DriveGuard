# Builder stage
FROM python:3.12-slim AS builder

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# Runner stage
FROM python:3.12-slim AS runner

WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos "" driveguarduser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/driveguarduser/.local

# Copy application code
COPY . /app

# Set PATH and permissions
ENV PATH=/home/driveguarduser/.local/bin:$PATH
RUN chown -R driveguarduser:driveguarduser /app

USER driveguarduser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
