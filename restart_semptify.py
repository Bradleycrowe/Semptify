"""
Restart Semptify with Production Server (Waitress)
Stops any running instances and starts fresh
"""

import os
import sys
import signal
import psutil
import subprocess
import time

def kill_semptify_processes():
    """Kill any running Semptify processes"""
    killed = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if cmdline and any('Semptify.py' in str(cmd) or 'run_prod.py' in str(cmd) for cmd in cmdline):
                print(f"🔴 Killing process {proc.info['pid']}: {proc.info['name']}")
                proc.kill()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return killed

def check_port_in_use(port=5000):
    """Check if port is in use"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == 'LISTEN':
            return True
    return False

def start_production_server():
    """Start Semptify with Waitress production server"""
    
    # Check if run_prod.py exists
    if os.path.exists('run_prod.py'):
        print("🚀 Starting with run_prod.py (Waitress)...")
        cmd = [sys.executable, 'run_prod.py']
    else:
        print("⚠️  run_prod.py not found, starting with Semptify.py...")
        cmd = [sys.executable, 'Semptify.py']
    
    # Start the process
    process = subprocess.Popen(cmd, 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True,
                               bufsize=1)
    
    return process

def main():
    print("=" * 60)
    print("🔄 RESTARTING SEMPTIFY WITH PRODUCTION SERVER")
    print("=" * 60)
    print()
    
    # Step 1: Kill existing processes
    print("🛑 Step 1: Stopping existing Semptify processes...")
    killed = kill_semptify_processes()
    if killed > 0:
        print(f"   ✅ Killed {killed} process(es)")
        time.sleep(2)  # Wait for ports to free up
    else:
        print("   ℹ️  No existing processes found")
    print()
    
    # Step 2: Check port
    print("🔍 Step 2: Checking port 5000...")
    if check_port_in_use(5000):
        print("   ⚠️  Port 5000 still in use, waiting...")
        time.sleep(3)
        if check_port_in_use(5000):
            print("   ❌ Port still in use after waiting. Manual intervention may be needed.")
            print("   Run: netstat -ano | findstr :5000")
            return
    else:
        print("   ✅ Port 5000 is available")
    print()
    
    # Step 3: Start production server
    print("🚀 Step 3: Starting production server...")
    print()
    
    process = start_production_server()
    
    # Monitor startup for a few seconds
    print("📋 Startup Log:")
    print("-" * 60)
    
    start_time = time.time()
    while time.time() - start_time < 5:
        line = process.stdout.readline()
        if line:
            print(line.rstrip())
            if 'Serving on' in line or 'Running on' in line:
                break
    
    print("-" * 60)
    print()
    print("✅ SEMPTIFY RESTARTED!")
    print()
    print("🌐 Access at:")
    print("   http://localhost:5000")
    print("   http://localhost:5000/hub")
    print("   http://localhost:5000/jurisdiction/dashboard")
    print()
    print("💡 Server running in background. Check Task Manager to stop.")
    print()

if __name__ == "__main__":
    main()
