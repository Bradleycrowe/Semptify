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

# Start Ollama server and pull llama3 model
CMD ["/bin/sh", "-c", "ollama serve & sleep 10 && ollama pull llama3 && tail -f /dev/null"]
