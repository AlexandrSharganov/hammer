FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY /app .

# # Expose port
# EXPOSE 8000

# Default command (can be overridden in docker-compose.yml)
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]