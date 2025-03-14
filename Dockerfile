# Use Python 3.12.3 as the base image
FROM python:3.12.3

# Set the working directory inside the container
WORKDIR /app

# Copy application code
COPY . /app

# Remove existing virtual environment if it exists
RUN if [ -d "/app/.venv" ]; then rm -rf /app/.venv; fi

# Create a new virtual environment
RUN python -m venv /app/.venv

# Install dependencies
RUN /app/.venv/bin/pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN /app/.venv/bin/pip install -r requirements.txt

# Install gnupg2 to fix GPG error
RUN apt-get update && apt-get install -y gnupg2

# Update Debian GPG keys
RUN curl -fsSL https://ftp-master.debian.org/keys/archive-key-8.asc | tee /etc/apt/trusted.gpg.d/debian-archive-key.asc

# Install ping and netcat for debugging and network testing
RUN apt-get update && apt-get install -y iputils-ping netcat-openbsd

# Set environment variables for Python
ENV PATH="/app/.venv/bin:$PATH"

# Copy the .env file to the container
COPY .env /app/.env

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]