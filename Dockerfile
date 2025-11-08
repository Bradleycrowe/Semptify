# Multi-stage Dockerfile - FORCE REBUILD: 2025-11-08-v2
FROM python:3.11-slim AS builder
ARG GIT_SHA="dev"
ARG BUILD_TIME="unknown"
ARG CACHE_BUST="2025-11-08-v2"
WORKDIR /app

# Verify Python version
RUN python --version && python --version | grep "3.11" || (echo "ERROR: Wrong Python version!" && exit 1)

# Install build/test dependencies and app requirements (cached separately from source)
COPY requirements.txt ./
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt

# Copy source for testing
COPY . /app

# (Optional) Omit running tests during image build to speed up deploys on Render
# Tests are run in CI; keeping image build lean reduces failures due to transient CI vs builder differences.

### Final image (runtime)
FROM python:3.11-slim AS runtime
ARG GIT_SHA="dev"
ARG BUILD_TIME="unknown"
ARG CACHE_BUST="2025-11-08-v2"
ENV GIT_SHA=${GIT_SHA} \
	BUILD_TIME=${BUILD_TIME} \
	CACHE_BUST=${CACHE_BUST}
WORKDIR /app

# Copy pre-installed dependencies from builder to avoid re-install (smaller & faster)
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only necessary application code (exclude caches & tests for smaller runtime image)
COPY . /app
RUN rm -rf /app/tests /app/__pycache__ || true
 # Do not ship any committed tokens file; enforced mode will bootstrap from ADMIN_TOKEN if needed
RUN rm -f /app/security/admin_tokens.json || true

EXPOSE 8080
CMD ["python", "./run_prod.py"]
