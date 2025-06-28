FROM python:3.11-slim

WORKDIR /app

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y openssl curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up environment variables for non-root user
ENV HOME=/home/appuser
ENV PYTHONUSERBASE=/home/appuser/.local
ENV PYTHONPATH=/home/appuser/.local/lib/python3.11/site-packages:/app
ENV PATH=/home/appuser/.local/bin:$PATH

# Set Git executable path for GitPython
ENV GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

# Create necessary directories and set permissions
RUN mkdir -p /app/.prisma/binaries && \
    mkdir -p /app/.prisma/engine && \
    mkdir -p /app/.prisma/cache && \
    mkdir -p /home/appuser/.local/lib/python3.11/site-packages

RUN chown -R appuser:appuser /app && \
    chown -R appuser:appuser /home/appuser

# Copy files
COPY . /app/

# Fix permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user for installations
USER appuser

# Install Python dependencies including Prisma
RUN pip install --user -r requirements.txt && \
    pip install --user prisma


WORKDIR /app/prisma

RUN python -m prisma generate && \
    # Ensure the binary is copied to our specified location
    cp -r /home/appuser/.local/lib/python3.11/site-packages/prisma/binaries /app/.prisma/binaries && \
    chmod +x /app/.prisma/binaries && \
    # Ensure the query engine is copied to our specified location
    cp -r /home/appuser/.local/lib/python3.11/site-packages/prisma/engine /app/.prisma/engine && \
    chmod +x /app/.prisma/engine

WORKDIR /app

EXPOSE 8001

# Set environment variables
ENV PRISMA_BINARY_CACHE_DIR=/app/.prisma/cache

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]