FROM python:3.12-slim

# Install system dependencies: ffmpeg cho yt-dlp, build tools cho curl-cffi
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    gcc \
    g++ \
    make \
    libcurl4-openssl-dev \
    libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements và install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run bot
CMD ["python", "main.py"]
