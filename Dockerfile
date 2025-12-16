FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY main.py .
COPY routers/ routers/
COPY static/ static/

# Create directories
RUN mkdir -p uploads logs

# Environment
ENV PORT=8000
ENV STORAGE_TYPE=r2

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
