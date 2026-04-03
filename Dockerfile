# Layered filesystem
# Reproducible builds
# Difference between COPY, RUN, CMD
# Why 0.0.0.0 is required in containers

# Multi-stage Docker build for FastAPI microservice

# 1. Base image create the build stage
FROM python:3.11-slim AS builder

# 2. Set working directory
WORKDIR /app
# 3. Copy dependency file
COPY requirements.txt .
# 4. Install dependencies
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# final runtime image smaller
# start with a clean image

FROM python:3.11-slim

# set working directory
WORKDIR /app

# # Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# copy application code
COPY app.py .

# 6. Expose port
EXPOSE 8000

# 7. Start the microservice(server)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]