# Multi-stage Dockerfile
FROM python:3.13-slim AS builder
ARG GIT_SHA="dev"
ARG BUILD_TIME="unknown"
WORKDIR /app

# Install build/test dependencies and app requirements (cached separately from source)
COPY requirements.txt ./
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt

# Copy source for testing
COPY . /app

# (Optional) Omit running tests during image build to speed up deploys on Render
# Tests are run in CI; keeping image build lean reduces failures due to transient CI vs builder differences.

### Final image (runtime)
FROM python:3.13-slim AS runtime
ARG GIT_SHA="dev"
ARG BUILD_TIME="unknown"
ENV GIT_SHA=${GIT_SHA} \
	BUILD_TIME=${BUILD_TIME}
WORKDIR /app

# Copy pre-installed dependencies from builder to avoid re-install (smaller & faster)
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only necessary application code (exclude caches & tests for smaller runtime image)
COPY . /app
RUN rm -rf /app/tests /app/__pycache__ || true

EXPOSE 8080
CMD ["python", "./run_prod.py"]
