# Use the official Python image from the Docker Hub
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    libnss3 \
    libgbm-dev \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libasound2 \
    fonts-liberation \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Set environment variables for the bot (replace these with your actual values)
ENV API_ID=29920508
ENV API_HASH=10676e77085a5214bcea5ca17cda5778
ENV BOT_TOKEN=7004352885:AAFCjjO0qFVliIaEY1KF_bAqbiYKoPGeqJc

# Command to run the application
CMD ["python", "main.py"]
