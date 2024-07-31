# Use the official Python image from the Docker Hub
FROM python:3.11-slim

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
