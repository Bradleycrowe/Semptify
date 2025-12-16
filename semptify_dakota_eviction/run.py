#!/usr/bin/env python3
"""
Dakota County Eviction Defense Module - Run Script
Starts the FastAPI server on port 8001 (separate from main Semptify on 8000)
"""

import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🏠 Starting Dakota County Eviction Defense Module")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )
