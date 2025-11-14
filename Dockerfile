FROM ollama/ollama:latest

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_MODELS=/root/.ollama/models

# Create models directory
RUN mkdir -p /root/.ollama/models

# Expose Ollama port
EXPOSE 11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:11434/api/tags || exit 1

# Start Ollama server
CMD ["ollama", "serve"]
