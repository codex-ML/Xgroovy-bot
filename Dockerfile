# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libxkbcommon-x11-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgtk-3-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libwayland-client0 \
    libwayland-server0 \
    libxshmfence1 \
    xdg-utils \
    libx11-xcb1 \
    libgstreamer1.0-0 \
    libatomic1 \
    libxslt1.1 \
    libvpx7 \
    libevent-2.1-7 \
    libopus0 \
    libgstreamer-plugins-base1.0-0 \
    libharfbuzz0b \
    libenchant2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    libflite1 \
    libpsl5 \
    libnghttp2-14 \
    libgles2 \
    libx264-155 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN python -m playwright install

# Copy the rest of the application code
COPY . /app/

# Run the bot
CMD ["python", "main.py"]
