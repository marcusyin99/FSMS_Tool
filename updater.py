import requests
import os
import subprocess
import sys

# CONFIGURATION
GITHUB_RAW_URL = "https://raw.githubusercontent.com/marcusyin99/FSMS_Tool/main/"
# Expanded list to include the updater itself and requirements
FILES_TO_UPDATE = ["app.py", "fsms_logic.py", "warranty_checker.py", "efsr_grabber.py", "updater.py", "requirements.txt"]
VERSION_FILE = "version.txt"

def get_local_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    return "0.0.0"

def update():
    print("Checking for updates...")
    try:
        response = requests.get(GITHUB_RAW_URL + VERSION_FILE, timeout=5)
        if response.status_code != 200:
            print("Could not reach update server.")
            return

        remote_version = response.text.strip()
        local_version = get_local_version()

        if remote_version != local_version:
            print(f"New version found: {remote_version} (Local: {local_version})")
            
            req_updated = False
            for filename in FILES_TO_UPDATE:
                print(f"Updating {filename}...")
                file_resp = requests.get(GITHUB_RAW_URL + filename, timeout=10)
                if file_resp.status_code == 200:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(file_resp.text)
                    if filename == "requirements.txt":
                        req_updated = True
                else:
                    print(f"Failed to download {filename}")
            
            # If requirements.txt changed, automatically install new packages
            if req_updated:
                print("New dependencies detected. Installing...")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
                except Exception as e:
                    print(f"Pip install failed: {e}")

            with open(VERSION_FILE, "w") as f:
                f.write(remote_version)
            
            print("Update complete!")
        else:
            print("App is up to date.")
            
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    update()
