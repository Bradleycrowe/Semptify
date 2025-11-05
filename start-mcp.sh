#!/bin/bash
# Quick start script for Render MCP

echo "🚀 Render MCP Quick Start"
echo "========================"
echo ""

# Check for API key
if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ Error: RENDER_API_KEY not set"
    echo ""
    echo "Get your API key from: https://dashboard.render.com"
    echo "1. Go to Account Settings"
    echo "2. Find API Keys section"
    echo "3. Create new API key"
    echo "4. Set: export RENDER_API_KEY=\"rnd_xxxxx\""
    exit 1
fi

# Check for Service ID
if [ -z "$RENDER_SERVICE_ID" ]; then
    echo "❌ Error: RENDER_SERVICE_ID not set"
    echo ""
    echo "Get your Service ID from: https://dashboard.render.com"
    echo "1. Go to your Semptify service"
    echo "2. Click Settings"
    echo "3. Find Service ID"
    echo "4. Set: export RENDER_SERVICE_ID=\"srv_xxxxx\""
    exit 1
fi

echo "✅ RENDER_API_KEY: ${RENDER_API_KEY:0:10}..."
echo "✅ RENDER_SERVICE_ID: $RENDER_SERVICE_ID"
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Install from: https://nodejs.org"
    exit 1
fi

echo "✅ Node.js: $(node --version)"
echo ""

# Start MCP server
echo "🌍 Starting Render MCP Server on port 3000..."
echo ""
node mcp-render-server.js
