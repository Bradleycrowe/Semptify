# Force rebuild: 2025-11-16 engine refactor
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Verify engines directory exists
RUN ls -la /app/engines/ || echo "ERROR: engines directory missing"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "run_prod.py"]
