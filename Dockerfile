# Use the official Python 3.11.5 slim image as the base
FROM python:3.11.12-slim

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /

# Install system dependencies and FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    ffmpeg \
    libmagic-dev \
    libopus0 \
    libffi-dev \
    libnacl-dev \
    libssl-dev \
    gcc && \
    rm -rf /var/lib/apt/lists/*


# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Command to run your application
CMD ["python", "connect.py"]
