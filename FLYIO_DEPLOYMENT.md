# Fly.io Ollama Deployment Guide

## Prerequisites
1. Install Fly.io CLI:
   ```powershell
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. Sign up/login to Fly.io:
   ```powershell
   fly auth signup
   # or
   fly auth login
   ```

## Deployment Steps

### 1. Create Volume (Persistent Storage for Models)
```powershell
fly volumes create ollama_data --size 3 --region ord
```

### 2. Deploy Ollama Service
```powershell
fly launch --config fly.toml --no-deploy
fly deploy --config fly.toml
```

### 3. Get Your Ollama URL
```powershell
fly status
# Note the hostname, e.g., semptify-ollama.fly.dev
```

### 4. Update Semptify Environment Variables
In your Render dashboard or .env file:
```
OLLAMA_URL=https://semptify-ollama.fly.dev
OLLAMA_MODEL=llama3
```

### 5. Verify Ollama is Running
```powershell
curl https://semptify-ollama.fly.dev/api/tags
```

## Monitoring & Management

### Check Logs
```powershell
fly logs
```

### SSH into Container
```powershell
fly ssh console
```

### Scale Resources (if needed)
```powershell
fly scale memory 4096  # Increase to 4GB for larger models
fly scale count 2      # Add more instances
```

## Cost Breakdown
- **Free Tier**: 3 shared-cpu-1x VMs + 3GB storage = $0/month
- **Current Config**: 1 VM @ 2GB RAM + 3GB volume = $0/month (within free tier)
- **If Upgrading**: 4GB RAM = ~$8/month

## Troubleshooting

### Model Not Loaded
```powershell
fly ssh console
ollama pull llama3
```

### Out of Memory
Edit fly.toml:
```toml
[[vm]]
  memory_mb = 4096  # Increase from 2048
```
Then: `fly deploy`

### Check Health
```powershell
fly checks list
```

## Alternative Regions
Change `primary_region` in fly.toml:
- `ord` - Chicago
- `iad` - Virginia
- `lax` - Los Angeles
- `fra` - Frankfurt
- `syd` - Sydney

## Next Steps
1. Deploy this Ollama service to Fly.io (commands above)
2. Get the public URL from `fly status`
3. Update OLLAMA_URL in your Semptify Render environment
4. Test from Semptify /laws page → AI Summary

Your AI summarization will now work in production! 🚀
