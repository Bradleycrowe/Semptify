# Multi-stage Dockerfile
FROM python:3.13-slim AS builder
ARG GIT_SHA="dev"
ARG BUILD_TIME="unknown"
WORKDIR /app

# Install build/test dependencies and app requirements
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy source for testing
COPY . /app

# Install pytest and run tests during the build to fail fast
RUN pip install --no-cache-dir pytest && pytest -q tests

### Final image (runtime)
FROM python:3.13-slim
ARG GIT_SHA="dev"
ARG BUILD_TIME="unknown"
ENV GIT_SHA=${GIT_SHA} \
	BUILD_TIME=${BUILD_TIME}
WORKDIR /app

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

EXPOSE 8080
CMD ["python", "./run_prod.py"]
