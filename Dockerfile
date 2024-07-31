# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y 
# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright
RUN pip install playwright

# Install Playwright system dependencies
RUN playwright install-deps

# Install Playwright browsers
RUN playwright install

# Copy the rest of the application code
COPY . /app/

# Run the bot
CMD ["python", "main.py"]
