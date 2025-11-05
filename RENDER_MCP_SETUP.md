# 🔗 Render MCP (Model Context Protocol) Setup Guide

## What is Render MCP?

Model Context Protocol (MCP) allows AI tools and coding agents to interact with your Render deployment directly. This enables:

- ✅ Check deployment status from AI tools
- ✅ View logs and metrics
- ✅ Trigger new deployments
- ✅ Manage environment variables
- ✅ Monitor performance

---

## Prerequisites

1. **Render Account** with Semptify service deployed
2. **Render API Key** (create in Render Dashboard)
3. **Service ID** (found in Render Dashboard)
4. **Node.js** installed (for MCP server)

---

## Step 1: Get Your Render API Key

### In Render Dashboard:

1. Go to https://dashboard.render.com
2. Click **Account Settings** (top right)
3. Scroll to **API Keys**
4. Click **Create API Key**
5. Copy the key (save securely!)

Example: `rnd_xxxxxxxxxxxxxxxxxxxxx`

---

## Step 2: Get Your Service ID

### In Render Dashboard:

1. Go to your Semptify service
2. Click **Settings**
3. Find **Service ID** (looks like: `srv-xxxxxxxxxxxxx`)
4. Copy and save it

---

## Step 3: Configure Environment Variables

Set these in your development environment:

### PowerShell:
```powershell
$env:RENDER_API_KEY = "rnd_xxxxxxxxxxxxxxxxxxxxx"
$env:RENDER_SERVICE_ID = "srv-xxxxxxxxxxxxx"
$env:MCP_PORT = "3000"
```

### Windows Command Prompt:
```cmd
set RENDER_API_KEY=rnd_xxxxxxxxxxxxxxxxxxxxx
set RENDER_SERVICE_ID=srv-xxxxxxxxxxxxx
set MCP_PORT=3000
```

### Linux/Mac:
```bash
export RENDER_API_KEY="rnd_xxxxxxxxxxxxxxxxxxxxx"
export RENDER_SERVICE_ID="srv-xxxxxxxxxxxxx"
export MCP_PORT="3000"
```

---

## Step 4: Start the MCP Server

```powershell
cd c:\repos git\UTAV\Semptify
node mcp-render-server.js
```

**Expected output:**
```
🚀 Render MCP Server listening on port 3000
Service ID: srv-xxxxxxxxxxxxx
```

---

## Step 5: Configure in VS Code or Your MCP Client

### In VS Code Settings (`settings.json`):

```json
{
  "mcpServers": {
    "render": {
      "command": "node",
      "args": ["c:/repos git/UTAV/Semptify/mcp-render-server.js"],
      "env": {
        "RENDER_API_KEY": "rnd_xxxxxxxxxxxxxxxxxxxxx",
        "RENDER_SERVICE_ID": "srv-xxxxxxxxxxxxx"
      }
    }
  }
}
```

### In Claude/Copilot MCP Config:

Add to your `.cursor/config.json` or similar:

```json
{
  "mcpServers": {
    "render": {
      "command": "node",
      "args": ["./mcp-render-server.js"],
      "env": {
        "RENDER_API_KEY": "${RENDER_API_KEY}",
        "RENDER_SERVICE_ID": "${RENDER_SERVICE_ID}"
      }
    }
  }
}
```

---

## Available Tools

Once configured, you can use these tools via MCP:

### 1. **get_render_status**
Get current deployment status and health
```
→ Status, URL, metrics, resource usage
```

### 2. **get_deployments**
View recent deployment history
```
Parameters: limit (default: 10)
→ List of recent deploys with timestamps and statuses
```

### 3. **get_logs**
Retrieve service logs
```
Parameters: limit (default: 100)
→ Recent log lines from your app
```

### 4. **trigger_deploy**
Manually trigger a new deployment
```
→ Initiates new build and deploy
```

### 5. **get_env_vars**
List all environment variables
```
→ Current env vars (secrets masked)
```

### 6. **update_env_var**
Update an environment variable
```
Parameters: key, value
→ Updates and redeploys if needed
```

### 7. **get_metrics**
Get performance metrics
```
→ CPU, memory, disk, requests/sec
```

---

## Usage Examples

### Check Deployment Status
```
"Can you check if Semptify is running on Render?"
→ Tool: get_render_status
→ Returns: Current status, URL, uptime
```

### View Recent Logs
```
"Show me the last 50 log lines from Semptify"
→ Tool: get_logs(limit=50)
→ Returns: Recent application logs
```

### Trigger Deployment
```
"Deploy the latest version of Semptify"
→ Tool: trigger_deploy
→ Returns: New deployment initiated
```

### Update Configuration
```
"Update SECURITY_MODE to enforced on Render"
→ Tool: update_env_var(key='SECURITY_MODE', value='enforced')
→ Returns: Update successful, redeploy initiated
```

---

## Troubleshooting

### "Connection refused" Error
- ✅ Verify MCP server is running: `node mcp-render-server.js`
- ✅ Check port 3000 is available
- ✅ Verify `RENDER_API_KEY` and `RENDER_SERVICE_ID` are set

### "Unauthorized" Error
- ✅ Check API key is valid (create new one in Render Dashboard)
- ✅ Verify service ID is correct
- ✅ Ensure API key hasn't expired

### "Service not found" Error
- ✅ Verify service ID matches your Semptify service
- ✅ Check service ID in Render Dashboard → Settings

### "No logs available" Error
- ✅ Service may be sleeping (free tier)
- ✅ Try triggering an action to generate logs
- ✅ Check logs directly in Render Dashboard

---

## Security Best Practices

⚠️ **NEVER commit these to Git:**
- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`
- Any secrets in `.mcp-config.json`

✅ **DO:**
- Use environment variables
- Store secrets in `.env` (add to `.gitignore`)
- Use Render's Secrets Manager for production
- Rotate API keys regularly

---

## Advanced: Running MCP in Production

### Option 1: Docker Container
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY mcp-render-server.js .
CMD ["node", "mcp-render-server.js"]
```

### Option 2: SystemD Service (Linux)
```ini
[Unit]
Description=Render MCP Server
After=network.target

[Service]
Type=simple
User=app
ExecStart=/usr/bin/node /app/mcp-render-server.js
Environment="RENDER_API_KEY=rnd_xxx"
Environment="RENDER_SERVICE_ID=srv_xxx"
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## Next Steps

1. ✅ Get API key and Service ID
2. ✅ Set environment variables
3. ✅ Start MCP server: `node mcp-render-server.js`
4. ✅ Configure in your AI tool
5. ✅ Start using Render tools!

---

## Support

- **Render Docs:** https://render.com/docs
- **MCP Specification:** https://modelcontextprotocol.io
- **Render API Docs:** https://api-docs.render.com

Your MCP server is ready! 🚀
