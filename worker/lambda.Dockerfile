FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y openssl curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV HOME=/home/appuser
ENV PYTHONUSERBASE=/home/appuser/.local
ENV PYTHONPATH=/home/appuser/.local/lib/python3.11/site-packages:/app
ENV PATH=/home/appuser/.local/bin:$PATH
ENV GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

# Create necessary dirs
RUN mkdir -p /app/.prisma/binaries /app/.prisma/engine /app/.prisma/cache \
 && mkdir -p /home/appuser/.local/lib/python3.11/site-packages \
 && chown -R appuser:appuser /app /home/appuser

# Copy project files
COPY . /app/
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Install Python dependencies and Prisma
RUN pip install --user --upgrade pip && \
    pip install --user prisma && \
    pip install --user -r requirements.txt && \
    pip install --user awslambdaric

# Generate Prisma client
WORKDIR /app/prisma
RUN python -m prisma generate && \
    cp -r /home/appuser/.local/lib/python3.11/site-packages/prisma/binaries /app/.prisma/binaries && \
    cp -r /home/appuser/.local/lib/python3.11/site-packages/prisma/engine /app/.prisma/engine && \
    chmod +x /app/.prisma/binaries/* || true && \
    chmod +x /app/.prisma/engine/* || true

WORKDIR /app

# Set Prisma ENV
ENV PRISMA_BINARY_CACHE_DIR=/app/.prisma/cache

# Copy handler startup script
COPY entry.sh /entry.sh
USER root
RUN chmod +x /entry.sh
USER appuser

# This is your function entry point
CMD ["/entry.sh"]
