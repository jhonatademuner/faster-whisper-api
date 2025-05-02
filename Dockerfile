FROM python:3.10-slim

# Avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure logs are output immediately (no buffering)
ENV PYTHONUNBUFFERED 1

# Install system dependencies: compiler, Python headers, ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
