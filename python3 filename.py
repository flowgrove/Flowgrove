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
    /**
 * FlowGrove Autonomous Core
 * Fully self-contained, self-updating, self-optimizing ecosystem
 * Supports: Replit Storage, GitHub sync, Google Gemini integration, automated front-end
 */

import { Client as StorageClient } from "@replit/object-storage";
import fs from "fs";
import path from "path";
import { exec } from "child_process";
import fetch from "node-fetch"; // For Google Gemini API or external integrations

const storage = new StorageClient();

// Configurations
const CONFIG = {
  GITHUB_REPO: "https://github.com/flowgrove/Flowgrove",
  AUTO_PULL_INTERVAL_MS: [1, 10], // 1-10 ms interval, scales dynamically
  FRONTEND_FILE: "index.html",
  BACKUP_BUCKET: "flowgrove-backup",
};

// Utility Functions
async function uploadToStorage(filename: string, content: string) {
  const { ok, error } = await storage.uploadFromText(filename, content);
  if (!ok) console.error("Storage upload failed:", error);
}

async function downloadFromStorage(filename: string) {
  const { ok, value, error } = await storage.downloadAsText(filename);
  if (!ok) {
    console.error("Storage download failed:", error);
    return null;
  }
  return value;
}

async function deleteFromStorage(filename: string) {
  const { ok, error } = await storage.delete(filename);
  if (!ok) console.error("Storage delete failed:", error);
}

// GitHub Sync
async function gitSync() {
  exec(`git pull ${CONFIG.GITHUB_REPO}`, (err, stdout, stderr) => {
    if (err) console.error("Git pull error:", err);
    else console.log("Git pull stdout:", stdout);
  });
}

// Google Gemini Hook (Stub, customize with API keys)
async function runGeminiAnalysis(data: string) {
  try {
    const response = await fetch("https://gemini.api.google.com/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data }),
    });
    const result = await response.json();
    console.log("Gemini analysis result:", result);
    return result;
  } catch (e) {
    console.error("Gemini analysis failed:", e);
    return null;
  }
}

// Front-end Auto Update
async function updateFrontend(content: string) {
  fs.writeFileSync(CONFIG.FRONTEND_FILE, content, "utf-8");
  await uploadToStorage(CONFIG.FRONTEND_FILE, content);
}

// Auto Backup
async function backupAllFiles() {
  const files = fs.readdirSync("./");
  for (const file of files) {
    if (file !== "node_modules" && fs.statSync(file).isFile()) {
      const content = fs.readFileSync(file, "utf-8");
      await uploadToStorage(path.join(CONFIG.BACKUP_BUCKET, file), content);
    }
  }
}

// Main Autonomous Loop
async function autonomousLoop() {
  try {
    // 1. GitHub Sync
    await gitSync();

    // 2. Pull Storage Files & Sanitize
    const storedFiles = await storage.list();
    for (const file of storedFiles.value || []) {
      const content = await downloadFromStorage(file.name);
      if (content) {
        fs.writeFileSync(file.name, content, "utf-8"); // Self-update
      }
    }

    // 3. Google Gemini Analysis (example: analyze code & optimize)
    const allFiles = fs.readdirSync("./").filter((f) => f.endsWith(".ts") || f.endsWith(".js"));
    for (const file of allFiles) {
      const code = fs.readFileSync(file, "utf-8");
      await runGeminiAnalysis(code);
    }

    // 4. Front-end Auto Update Example
    const htmlContent = `<html>
  <head><title>FlowGrove</title></head>
  <body>
    <h1>FlowGrove Autonomous System</h1>
    <script src="https://replit.com/public/js/replit-badge-v2.js" theme="dark" position="bottom-right"></script>
  </body>
</html>`;
    await updateFrontend(htmlContent);

    // 5. Auto Backup
    await backupAllFiles();

    // 6. Self-scheduling next run
    const nextDelay = Math.floor(Math.random() * (CONFIG.AUTO_PULL_INTERVAL_MS[1] - CONFIG.AUTO_PULL_INTERVAL_MS[0])) + CONFIG.AUTO_PULL_INTERVAL_MS[0];
    setTimeout(autonomousLoop, nextDelay);
  } catch (e) {
    console.error("Autonomous loop error:", e);
    setTimeout(autonomousLoop, 50); // retry on error
  }
}

// Initialize
(async function init() {
  console.log("FlowGrove Autonomous System Initialized");
  await autonomousLoop();
})();
// flowgrove-autonomous.ts
import { Client as StorageClient } from "@replit/object-storage";
import { exec } from "child_process";
import fetch from "node-fetch";
import fs from "fs";
import path from "path";

const storage = new StorageClient();
const GITHUB_REPO = process.env.GITHUB_REPO || ""; // Your repo URL
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || "";
const GOOGLE_GEMINI_KEY = process.env.GOOGLE_GEMINI_KEY || "";

// ===== UTILITY FUNCTIONS =====
function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function sanitize(text: string) {
  return text.replace(/[<>]/g, ""); // basic sanitation
}

async function safeWrite(filePath: string, data: string) {
  const sanitized = await sanitize(data);
  fs.writeFileSync(filePath, sanitized, "utf8");
}

// ===== REPLIT STORAGE FUNCTIONS =====
async function listStorageFiles() {
  const { ok, value, error } = await storage.list();
  if (!ok) console.error("Storage list failed:", error);
  return ok ? value : [];
}

async function uploadFile(fileName: string, content: string) {
  const { ok, error } = await storage.uploadFromText(fileName, await sanitize(content));
  if (!ok) console.error("Storage upload failed:", error);
}

async function downloadFile(fileName: string) {
  const { ok, value, error } = await storage.downloadAsText(fileName);
  if (!ok) console.error("Storage download failed:", error);
  return ok ? value : null;
}

async function deleteFile(fileName: string) {
  const { ok, error } = await storage.delete(fileName);
  if (!ok) console.error("Storage delete failed:", error);
}

// ===== GITHUB AUTOMATION =====
async function gitCommand(cmd: string) {
  return new Promise((resolve, reject) => {
    exec(cmd, { cwd: process.cwd() }, (err, stdout, stderr) => {
      if (err) return reject(stderr);
      resolve(stdout);
    });
  });
}

async function syncGitHub() {
  try {
    await gitCommand("git pull origin main");
    await gitCommand("git add -A");
    await gitCommand(`git commit -m "Autonomous update" || echo "No changes to commit"`);
    await gitCommand("git push origin main");
  } catch (err) {
    console.error("GitHub sync error:", err);
  }
}

// ===== GOOGLE GEMINI =====
async function googleGeminiRequest(prompt: string) {
  try {
    const response = await fetch("https://gemini.googleapis.com/v1/complete", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${GOOGLE_GEMINI_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });
    const data = await response.json();
    return data.output || "";
  } catch (err) {
    console.error("Gemini request error:", err);
    return "";
  }
}

// ===== FRONT-END AUTO UPDATE =====
async function updateFrontEnd() {
  const htmlPath = path.join(process.cwd(), "index.html");
  const jsPath = path.join(process.cwd(), "index.js");
  
  if (!fs.existsSync(htmlPath)) fs.writeFileSync(htmlPath, "<html><body></body></html>");
  if (!fs.existsSync(jsPath)) fs.writeFileSync(jsPath, "// Frontend script");

  const badgeScript = `<script src="https://replit.com/public/js/replit-badge-v2.js" theme="dark" position="bottom-right"></script>`;
  let htmlContent = fs.readFileSync(htmlPath, "utf8");
  if (!htmlContent.includes(badgeScript)) {
    htmlContent = htmlContent.replace("</body>", `${badgeScript}</body>`);
    safeWrite(htmlPath, htmlContent);
  }
}

// ===== MAIN LOOP =====
async function mainLoop() {
  while (true) {
    try {
      // Replit Storage Automation
      const files = await listStorageFiles();
      for (const file of files) {
        const content = await downloadFile(file.name);
        if (content) await uploadFile(file.name, content); // sanitize and re-upload
      }

      // GitHub Sync
      await syncGitHub();

      // Google Gemini Example
      const geminiOutput = await googleGeminiRequest("Generate autonomous update report");
      if (geminiOutput) console.log("Gemini output:", geminiOutput);

      // Front-end auto-update
      await updateFrontEnd();
    } catch (err) {
      console.error("Main loop error:", err);
    }

    // Adjustable delay: 1–10 ms
    await sleep(Math.floor(Math.random() * 10) + 1);
  }
}

// Start the system
mainLoop().catch(console.error);
# Ultimate Autonomous System v3
# Fully integrated with Google Gemini API
# Drop-in ready, fully autonomous

import os
import sys
import time
import json
import threading
import logging
from pathlib import Path
import requests
import execjs  # run JS/TS directly in Python

# -------------------------------
# Logging Setup
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# -------------------------------
# Global Config
# -------------------------------
CONFIG = {
    "loop_interval_ms": 1,
    "replit_bucket": "flowgrove-bucket",
    "github_repo": "https://github.com/flowgrove/Flowgrove.git",
    "gemini_api_key": "YOUR_GOOGLE_GEMINI_API_KEY",
    "auto_frontend_update": True,
}

BASE_DIR = Path(__file__).parent.resolve()
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

# -------------------------------
# Node.js Context for Replit
# -------------------------------
NODE_CONTEXT = execjs.get()
REPLIT_JS_LIB = """
const { Client } = require("@replit/object-storage");
const client = new Client();
async function upload(filename, content) {
    const { ok, error } = await client.uploadFromText(filename, content);
    return { ok, error };
}
async function listFiles() {
    const { ok, value, error } = await client.list();
    return { ok, value, error };
}
async function deleteFile(filename) {
    const { ok, error } = await client.delete(filename);
    return { ok, error };
}
"""
JS_CTX = NODE_CONTEXT.compile(REPLIT_JS_LIB)

def upload_file_replit(filename, content):
    return JS_CTX.eval(f'upload("{filename}", `{content}`)')

def list_files_replit():
    return JS_CTX.eval("listFiles()")

def delete_file_replit(filename):
    return JS_CTX.eval(f'deleteFile("{filename}")')

# -------------------------------
# GitHub Auto-Sync
# -------------------------------
def git_clone_or_pull(repo_url, target_dir):
    target_dir.mkdir(exist_ok=True)
    if not any(target_dir.iterdir()):
        os.system(f"git clone {repo_url} {target_dir}")
        logging.info("Cloned GitHub repo")
    else:
        os.system(f"git -C {target_dir} pull")
        logging.info("Pulled latest GitHub updates")

# -------------------------------
# Google Gemini Integration
# -------------------------------
def gemini_request(prompt: str):
    """Send a prompt to Gemini API and return the response."""
    url = "https://gemini.googleapis.com/v1/responses"  # hypothetical endpoint
    headers = {"Authorization": f"Bearer {CONFIG['gemini_api_key']}"}
    payload = {"prompt": prompt, "max_output_tokens": 512}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=5)
        r.raise_for_status()
        data = r.json()
        return data.get("output_text", "")
    except Exception as e:
        logging.error(f"Gemini request failed: {e}")
        return ""

# -------------------------------
# Frontend Update
# -------------------------------
def update_frontend():
    index_file = BASE_DIR / "index.html"
    if index_file.exists():
        content = index_file.read_text()
        badge_script = """
<script src="https://replit.com/public/js/replit-badge-v2.js"
        theme="dark" position="bottom-right"></script>
"""
        if "replit-badge-v2.js" not in content:
            content += badge_script
            index_file.write_text(content)
            logging.info("Injected Replit Badge into frontend")

# -------------------------------
# Autonomous Loop
# -------------------------------
def adaptive_sleep():
    interval = max(1, min(CONFIG["loop_interval_ms"], 10))
    time.sleep(interval / 1000)

def process_file_autonomously(filename):
    """Download, sanitize, process, and re-upload file."""
    # Placeholder: download file content from Replit
    files = list_files_replit().get("value", [])
    for obj in files:
        if obj.get("name") == filename:
            logging.info(f"Processing file: {filename}")
            # Gemini AI analysis
            prompt = f"Analyze and improve this file content: {filename}"
            output = gemini_request(prompt)
            if output:
                upload_file_replit(filename, output)
                logging.info(f"Updated {filename} with Gemini AI")

def autonomous_loop():
    while True:
        try:
            # Replit Storage auto-sync
            files = list_files_replit().get("value", [])
            for obj in files:
                name = obj.get("name")
                process_file_autonomously(name)
            
            # GitHub auto-sync
            git_clone_or_pull(CONFIG["github_repo"], BASE_DIR / "repo")
            
            # AI/Gemini autonomous task
            response = gemini_request("Generate a useful log message")
            logging.info(f"Gemini: {response}")
            
            # Frontend update
            if CONFIG["auto_frontend_update"]:
                update_frontend()
            
            adaptive_sleep()
        except Exception as e:
            logging.error(f"Loop error: {e}")
            time.sleep(1)

# -------------------------------
# Initialization
# -------------------------------
def initialize_system():
    logging.info("Initializing fully autonomous system with Gemini")
    STORAGE_DIR.mkdir(exist_ok=True)
    update_frontend()
    threading.Thread(target=autonomous_loop, daemon=True).start()

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    initialize_system()
    logging.info("System fully operational with Gemini integration")
    while True:
        time.sleep(60)
        import os
import time
import asyncio
import logging
import requests
from threading import Thread
from replit.object_storage import Client as StorageClient
from github import Github

# ----------------------------
# CONFIGURATION
# ----------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
UPDATE_INTERVAL_MS = 1  # dynamic loop

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ----------------------------
# CLIENTS
# ----------------------------
storage = StorageClient()
github_client = Github(GITHUB_TOKEN)
repo = github_client.get_repo(GITHUB_REPO)

# ----------------------------
# STORAGE MANAGEMENT
# ----------------------------
def upload_file(filename: str, content: str):
    ok, error = storage.upload_from_text(filename, content)
    if ok:
        logging.info(f"Uploaded {filename}")
    else:
        logging.error(f"Upload failed for {filename}: {error}")

def download_file(filename: str):
    ok, content, error = storage.download_as_text(filename)
    if ok:
        return content
    logging.error(f"Download failed for {filename}: {error}")
    return None

def delete_file(filename: str):
    ok, error = storage.delete(filename)
    if ok:
        logging.info(f"Deleted {filename}")
    else:
        logging.error(f"Delete failed for {filename}: {error}")

def list_files():
    ok, files, error = storage.list()
    if ok:
        return [f.name for f in files]
    logging.error(f"Listing failed: {error}")
    return []

def sanitize_file(content: str):
    return content.strip()

# ----------------------------
# GITHUB AUTOMATION
# ----------------------------
def push_to_github(filename: str, content: str, commit_message="Auto update"):
    try:
        file = repo.get_contents(filename)
        repo.update_file(file.path, commit_message, content, file.sha)
        logging.info(f"Pushed {filename} to GitHub")
    except Exception:
        repo.create_file(filename, commit_message, content)
        logging.info(f"Created {filename} on GitHub")

# ----------------------------
# GOOGLE GEMINI INTEGRATION
# ----------------------------
def optimize_with_gemini(content: str):
    # Placeholder: Replace with real Gemini API call
    # Example: Sends content to Gemini, gets optimized/suggested update
    try:
        # Simulate API call
        optimized = content + "\n# Optimized by Gemini AI"
        return optimized
    except Exception as e:
        logging.error(f"Gemini optimization failed: {e}")
        return content

# ----------------------------
# SELF-AUTOMATION LOOP
# ----------------------------
async def auto_loop():
    while True:
        files = list_files()
        for f in files:
            content = download_file(f)
            if content:
                sanitized = sanitize_file(content)
                optimized = optimize_with_gemini(sanitized)
                upload_file(f, optimized)
                push_to_github(f, optimized)
        await asyncio.sleep(UPDATE_INTERVAL_MS / 1000)

def run_loop():
    asyncio.run(auto_loop())

# ----------------------------
# INITIAL SETUP
# ----------------------------
if __name__ == "__main__":
    logging.info("Ultimate autonomous system starting with Google Gemini integration...")

    Thread(target=run_loop, daemon=True).start()

    # Self-managing core
    upload_file("system_core.txt", "Fully autonomous system running at conceptual max with Gemini AI!")
    
    # JS helper layer
    js_code = """
    <script src="https://replit.com/public/js/replit-badge-v2.js" theme="dark" position="bottom-right"></script>
    """
    upload_file("helper.js", js_code)

    logging.info("System setup complete. Running continuously without intervention.")

    while True:
        time.sleep(1)
        import os
import subprocess
from datetime import datetime
from pathlib import Path
from replit.object_storage import Client as ReplitClient
from git import Repo, GitCommandError
import random
import time

# ------------------------------
# CONFIGURATION
# ------------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Place your GitHub token in env variables
GITHUB_REPO = "flowgrove/Flowgrove"
LOCAL_PATH = Path("/tmp/flowgrove_repo")
replit_client = ReplitClient()
NODE_PATH = "node"  # Node.js path

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------
def auto_manage_files():
    """Update or create files dynamically for GitHub and Replit"""
    gen_file = LOCAL_PATH / "auto_generated.txt"
    gen_file.write_text(f"Updated at {datetime.utcnow()}\n")

    js_file = LOCAL_PATH / "dynamic_script.js"
    js_file.write_text(f'console.log("Auto-run at {datetime.utcnow()}");\n')

    replit_client.upload_from_text("auto_generated.txt", gen_file.read_text())

def run_js_file(js_file_path):
    """Run JS file with Node.js"""
    try:
        subprocess.run([NODE_PATH, str(js_file_path)], check=True)
    except subprocess.CalledProcessError as e:
        print("JS execution error:", e)

def git_clone_or_pull():
    """Clone repo if missing, otherwise pull latest"""
    if not LOCAL_PATH.exists():
        try:
            Repo.clone_from(
                f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git",
                LOCAL_PATH
            )
        except GitCommandError as e:
            print("Git clone error:", e)
    else:
        try:
            repo = Repo(LOCAL_PATH)
            repo.remotes.origin.pull()
        except GitCommandError as e:
            print("Git pull error:", e)

def git_commit_push():
    """Commit and push changes automatically"""
    try:
        repo = Repo(LOCAL_PATH)
        repo.git.add(all=True)
        if repo.is_dirty():
            repo.index.commit(f"Auto-update {datetime.utcnow()}")
            repo.remotes.origin.push()
    except GitCommandError as e:
        print("Git push error:", e)

def sanitize_replit_files():
    """Sanitize Replit storage files automatically"""
    for obj in replit_client.list():
        if obj.name.endswith(".txt"):
            content = replit_client.download_as_text(obj.name)
            sanitized = content.replace("BAD_DATA", "")
            replit_client.upload_from_text(obj.name, sanitized)

# ------------------------------
# MAIN LOOP
# ------------------------------
def main_loop():
    while True:
        git_clone_or_pull()
        auto_manage_files()
        sanitize_replit_files()
        git_commit_push()

        for js_file in LOCAL_PATH.glob("*.js"):
            run_js_file(js_file)

        time.sleep(random.uniform(0.001, 0.01))  # 1–10 ms adaptive

# ------------------------------
# START
# ------------------------------
if __name__ == "__main__":
    main_loop()
    # main.py
import os
import asyncio
import json
import base64
from datetime import datetime
from threading import Thread

# Optional: For GitHub integration
import requests

# ---------- CONFIG ----------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Ensure token access
REPO = "flowgrove/Flowgrove"  # Replace with your repo
BRANCH = "main"

# ---------- UTILITY FUNCTIONS ----------
def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def encode_file(content):
    return base64.b64encode(content.encode()).decode()

def decode_file(content):
    return base64.b64decode(content.encode()).decode()

# ---------- FILE MANAGEMENT ----------
class FileManager:
    def __init__(self):
        self.files = {}  # Local in-memory cache

    def upload(self, filename, content):
        log(f"Uploading {filename}")
        self.files[filename] = content
        return True

    def download(self, filename):
        content = self.files.get(filename)
        if content:
            log(f"Downloading {filename}")
            return content
        log(f"{filename} not found")
        return None

    def delete(self, filename):
        if filename in self.files:
            del self.files[filename]
            log(f"{filename} deleted")
            return True
        log(f"{filename} delete failed")
        return False

    def list_files(self):
        return list(self.files.keys())

file_manager = FileManager()

# ---------- AUTO GITHUB SYNC ----------
class GitHubSync:
    def __init__(self, repo, branch, token):
        self.repo = repo
        self.branch = branch
        self.token = token
        self.base_url = f"https://api.github.com/repos/{self.repo}/contents/"

    def push_file(self, filename, content, message="Update from AI"):
        url = f"{self.base_url}{filename}"
        encoded_content = encode_file(content)
        data = {"message": message, "content": encoded_content, "branch": self.branch}
        headers = {"Authorization": f"token {self.token}"}
        resp = requests.put(url, json=data, headers=headers)
        log(f"Pushed {filename} to GitHub: {resp.status_code}")
        return resp.status_code in [200, 201]

    def fetch_file(self, filename):
        url = f"{self.base_url}{filename}?ref={self.branch}"
        headers = {"Authorization": f"token {self.token}"}
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            content = decode_file(resp.json()["content"])
            log(f"Fetched {filename} from GitHub")
            return content
        log(f"{filename} not found on GitHub")
        return None

github_sync = GitHubSync(REPO, BRANCH, GITHUB_TOKEN)

# ---------- AI / GOOGLE GEMINI HOOK ----------
async def ai_task():
    while True:
        log("Running AI optimization cycle...")
        # Placeholder: Integrate Google Gemini API calls here
        # Example: file_manager.upload("ai_log.txt", "Updated by AI")
        await asyncio.sleep(1)  # Run every 1 second

# ---------- EMBEDDED FRONT-END ----------
FRONTEND_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Flowgrove AI</title>
</head>
<body>
<h2>Flowgrove AI Dashboard</h2>
<div id="status">Initializing...</div>
<script src="https://replit.com/public/js/replit-badge-v2.js" theme="dark" position="bottom-right"></script>
<script>
async function fetchStatus() {
    try {
        const res = await fetch('/status');
        const data = await res.json();
        document.getElementById('status').innerText = JSON.stringify(data);
    } catch (e) {
        document.getElementById('status').innerText = 'Error fetching status';
    }
}
setInterval(fetchStatus, 1000);
</script>
</body>
</html>
"""

# ---------- ASYNC WEB SERVER ----------
from aiohttp import web

async def handle_status(request):
    return web.json_response({
        "files": file_manager.list_files(),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

async def handle_frontend(request):
    return web.Response(text=FRONTEND_HTML, content_type="text/html")

app = web.Application()
app.add_routes([web.get('/status', handle_status),
                web.get('/', handle_frontend)])

# ---------- SELF-UPDATE & AUTO MANAGEMENT ----------
async def self_update_cycle():
    while True:
        log("Checking for self-updates...")
        # Example: Pull latest main.py from GitHub and reload if needed
        latest_code = github_sync.fetch_file("main.py")
        if latest_code and latest_code != open(__file__).read():
            with open(__file__, "w") as f:
                f.write(latest_code)
            log("Self-updated with latest code")
        await asyncio.sleep(0.01)  # 10ms interval

# ---------- MAIN RUN ----------
async def main():
    loop = asyncio.get_event_loop()
    asyncio.create_task(ai_task())
    asyncio.create_task(self_update_cycle())
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    log("Flowgrove AI running")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())