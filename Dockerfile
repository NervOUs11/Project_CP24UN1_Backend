# Use Python 3.12.3 as the base image
FROM python:3.12.3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy application code
COPY . /app

# Remove existing virtual environment if it exists
RUN if [ -d "/app/.venv" ]; then rm -rf /app/.venv; fi

# Create a new virtual environment
RUN python -m venv /app/.venv

# Install dependencies
RUN /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install -r requirements.txt

# Set environment variables for Python
ENV PATH="/app/.venv/bin:$PATH"

# Run the FastAPI application on port 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]