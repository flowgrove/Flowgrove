#!/usr/bin/env python3
import os
import sys
import time
import shutil
import subprocess
import logging
from pathlib import Path
from flask import Flask

# ========== Logging ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("system_master.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("MASTER")

# ========== Flask App ==========
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Fully Automated Intelligence Ecosystem Running"

# ========== Environment Detection ==========
def detect_environment():
    if "REPL_OWNER" in os.environ:
        return "replit"
    elif ".git" in os.listdir("."):
        return "github"
    else:
        return "local"

# ========== File Sanitizer ==========
def sanitize_files():
    safe_extensions = {".py", ".txt", ".md", ".json"}
    for root, _, files in os.walk("."):
        for f in files:
            path = Path(root) / f
            if path.suffix not in safe_extensions:
                try:
                    shutil.move(str(path), str(Path("sanitized") / f))
                    log.warning(f"Sanitized {f}")
                except Exception as e:
                    log.error(f"Failed to sanitize {f}: {e}")

# ========== Self-Updater ==========
def self_update():
    try:
        if detect_environment() == "github":
            subprocess.run(["git", "pull"], check=True)
            log.info("Pulled latest updates from GitHub")
        elif detect_environment() == "replit":
            log.info("Replit environment detected – syncing handled by Replit")
        else:
            log.info("Local mode – no remote sync configured")
    except Exception as e:
        log.error(f"Update failed: {e}")

# ========== File Grabber ==========
def grab_files():
    base = Path(".")
    collected = Path("collected_files")
    collected.mkdir(exist_ok=True)

    for root, _, files in os.walk(base):
        for f in files:
            src = Path(root) / f
            dst = collected / f
            if not dst.exists():
                try:
                    shutil.copy2(src, dst)
                    log.info(f"Grabbed file: {f}")
                except Exception as e:
                    log.error(f"Error grabbing {f}: {e}")

# ========== Main Loop ==========
def ecosystem_loop():
    while True:
        sanitize_files()
        grab_files()
        self_update()
        time.sleep(0.001)  # ~1ms loop

# ========== Entry ==========
if __name__ == "__main__":
    env = detect_environment()
    log.info(f"Running in {env} mode")

    # Start Flask in background
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))).start()

    # Run ecosystem
    ecosystem_loop()
    python3 filename.py