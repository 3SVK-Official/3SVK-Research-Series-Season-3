#!/usr/bin/env python3
"""
AetherMesh One-Click Launcher & Demo Runner
3SVK National Cloud & AI Innovation Challenge
"""

import sys
import os
import time
import webbrowser
import threading

# Ensure workspace and aethermesh packages are on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
PARENT_DIR = os.path.dirname(BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

BANNER = r"""
   ___       __  __            __  ___         __  
  / _ | ___ / /_/ /  ___ ____ /  |/  /__ ___  / /  
 / __ |/ -_) __/ _ \/ -_) __// /|_/ / -_|_-< / _ \ 
/_/ |_|\__/\__/_//_/\__/_/  /_/  /_/\__/___//_//_/ 

>> 3SVK NATIONAL CLOUD & AI INNOVATION CHALLENGE
>> Track: Cloud Infrastructure & Artificial Intelligence
>> Prototype: Autonomous Self-Healing Multi-Cloud Mesh (GNN + DRL)
========================================================================
"""

def open_browser():
    time.sleep(1.5)
    url = "http://127.0.0.1:8000"
    print(f"\n[AetherMesh Launcher] Opening Mission Control Dashboard: {url}")
    webbrowser.open(url)

def main():
    print(BANNER)
    print("[*] Initializing Spatio-Temporal GNN Engine...")
    print("[*] Initializing Deep Reinforcement Learning (DRL) Orchestrator...")
    print("[*] Connecting Multi-Cloud eBPF Telemetry Taps (AWS, GCP, Azure)...")
    print("[*] Mounting CRDT State Store across simulated regions...")
    print("\n[+] Starting FastAPI Web & WebSocket Server on http://127.0.0.1:8000 ...")

    # Start browser opener in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    from backend.app import app

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    main()
