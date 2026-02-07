# Use a slim Python image for a smaller footprint
FROM python:3.12-slim

# Install system dependencies for rawpy and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv directly from the official binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies into the system environment (ideal for Docker)
RUN uv sync --frozen --no-cache

# Copy the rest of the project
COPY . .

# Expose the Django port
EXPOSE 8000

# Default command (will be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]