"""
SemptifyStartApp.py - Single-button Windows launcher for Semptify.
Spawns production server, waits for readiness, opens GUI, and offers Stop button.
"""
import os, subprocess, threading, time, webbrowser, tkinter as tk
from tkinter import messagebox

SEMPTIFY_DIR = r"C:\Semptify\Semptify"
PORT = os.environ.get("SEMPTIFY_PORT", "8080")
PYTHON = os.path.join(SEMPTIFY_DIR, ".venv", "Scripts", "python.exe")
RUN_SCRIPT = os.path.join(SEMPTIFY_DIR, "run_prod.py")
ICON_PATH = os.path.join(SEMPTIFY_DIR, "semptify_icon.ico")

server_process = None
stop_requested = False

def server_running():
    import urllib.request
    try:
        with urllib.request.urlopen(f"http://localhost:{PORT}", timeout=1) as _:
            return True
    except Exception:
        return False

def start_server():
    global server_process
    if server_process and server_process.poll() is None:
        return
    env = os.environ.copy()
    env["SEMPTIFY_PORT"] = PORT
    server_process = subprocess.Popen([PYTHON, RUN_SCRIPT], cwd=SEMPTIFY_DIR, env=env)

def wait_for_server(timeout=25):
    start = time.time()
    while time.time() - start < timeout:
        if server_running():
            return True
        if stop_requested:
            return False
        time.sleep(1)
    return False

def launch():
    status_var.set("Starting server...")
    start_btn.config(state=tk.DISABLED)
    threading.Thread(target=_launch_thread, daemon=True).start()

def _launch_thread():
    try:
        if not server_running():
            start_server()
        status_var.set("Waiting for readiness...")
        ready = wait_for_server()
        if ready:
            status_var.set("Opening GUI in browser...")
            webbrowser.open(f"http://localhost:{PORT}/gui")
            status_var.set("Semptify running on port " + PORT)
            stop_btn.config(state=tk.NORMAL)
        else:
            status_var.set("Server failed to start")
            start_btn.config(state=tk.NORMAL)
    except Exception as e:
        status_var.set("Error: " + str(e))
        start_btn.config(state=tk.NORMAL)

def stop_server():
    global stop_requested
    stop_requested = True
    status_var.set("Stopping server...")
    if server_process and server_process.poll() is None:
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
    status_var.set("Server stopped")
    stop_btn.config(state=tk.DISABLED)
    start_btn.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Semptify Launcher")
root.geometry("360x240")
root.resizable(False, False)

try:
    root.iconbitmap(ICON_PATH)
except Exception:
    pass

header = tk.Label(root, text="Semptify", font=("Segoe UI", 20, "bold"))
header.pack(pady=8)
sub = tk.Label(root, text="Single-click start", font=("Segoe UI", 10))
sub.pack(pady=2)

status_var = tk.StringVar(value="Idle - click Start")
status_lbl = tk.Label(root, textvariable=status_var, wraplength=320, justify="center")
status_lbl.pack(pady=10)

start_btn = tk.Button(root, text="Start Semptify", width=18, height=2, command=launch, bg="#4A90E2", fg="white", font=("Segoe UI", 11, "bold"))
start_btn.pack(pady=6)

stop_btn = tk.Button(root, text="Stop", width=10, command=stop_server, state=tk.DISABLED)
stop_btn.pack(pady=4)

footer = tk.Label(root, text=f"Port: {PORT}", font=("Segoe UI", 8), fg="#555")
footer.pack(side="bottom", pady=6)

root.mainloop()
