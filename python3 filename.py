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
    import os
import sys
import time
import shutil
import json
import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path
from replit.object_storage import Client as StorageClient

# ----------------------------
# Config & Initialization
# ----------------------------
storage = StorageClient()
SNAPSHOT_DIR = Path("./snapshots")
PLUGIN_DIR = Path("./plugins")
GITHUB_REPO = "flowgrove/Flowgrove"  # your GitHub repo
UPDATE_INTERVAL_MS = 1  # Can auto-adjust if needed

# Ensure directories exist
SNAPSHOT_DIR.mkdir(exist_ok=True)
PLUGIN_DIR.mkdir(exist_ok=True)

# ----------------------------
# File Utilities
# ----------------------------
def sanitize_content(content: str) -> str:
    """Sanitize file content to prevent unsafe operations."""
    # Basic sanitization example
    return content.replace("import os.system", "# REMOVED for safety")

def save_snapshot(filename: str, content: str):
    """Save a snapshot of a file."""
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    snapshot_path = SNAPSHOT_DIR / f"{filename}_{ts}.snap"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        f.write(content)

def fetch_local_files():
    """Fetch and sanitize all Python files in the directory."""
    files_data = {}
    for file_path in Path(".").glob("*.py"):
        content = file_path.read_text(encoding="utf-8")
        sanitized = sanitize_content(content)
        save_snapshot(file_path.name, sanitized)
        files_data[file_path.name] = sanitized
    return files_data

async def fetch_storage_files():
    """Fetch files from Replit Object Storage and sanitize."""
    objects = await storage.list()
    files_data = {}
    for obj in objects:
        content = await storage.download_as_text(obj.name)
        sanitized = sanitize_content(content)
        files_data[obj.name] = sanitized
    return files_data

async def push_storage_files(files: dict):
    """Push files back to Replit storage."""
    for filename, content in files.items():
        await storage.upload_from_text(filename, content)

# ----------------------------
# GitHub Integration
# ----------------------------
async def github_pull_self_update():
    """Pull latest updates from GitHub."""
    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/main.py"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                content = await resp.text()
                content = sanitize_content(content)
                save_snapshot("main.py", content)
                with open("main.py", "w", encoding="utf-8") as f:
                    f.write(content)
                print("GitHub update applied.")
            else:
                print("GitHub pull failed:", resp.status)

# ----------------------------
# Plugin Management
# ----------------------------
def load_plugins():
    """Load and execute plugins automatically."""
    for plugin_file in PLUGIN_DIR.glob("*.py"):
        code = plugin_file.read_text(encoding="utf-8")
        exec(sanitize_content(code), globals())

# ----------------------------
# Main Loop
# ----------------------------
async def main_loop():
    while True:
        # 1. Fetch & store local files
        local_files = fetch_local_files()

        # 2. Fetch Replit storage files and update local
        storage_files = await fetch_storage_files()
        for fname, content in storage_files.items():
            if fname not in local_files:
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(content)
                save_snapshot(fname, content)

        # 3. Load plugins
        load_plugins()

        # 4. Push back all files to Replit storage
        await push_storage_files({**local_files, **storage_files})

        # 5. GitHub self-update
        await github_pull_self_update()

        # 6. Auto adjust interval if possible
        await asyncio.sleep(UPDATE_INTERVAL_MS / 1000)  # ms -> sec

# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    print("Ultimate autonomous intelligence system starting...")
    asyncio.run(main_loop())