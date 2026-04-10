import requests
import os

# CONFIGURATION
# Replace this URL with your actual Raw GitHub repository path
GITHUB_RAW_URL = "https://raw.githubusercontent.com/marcusyin99/FSMS_Tool/main/"
FILES_TO_UPDATE = ["app.py", "fsms_logic.py", "warranty_checker.py", "efsr_grabber.py"]
VERSION_FILE = "version.txt"

def get_local_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    return "0.0.0"

def update():
    print("Checking for updates...")
    try:
        # 1. Check Version
        response = requests.get(GITHUB_RAW_URL + VERSION_FILE, timeout=5)
        if response.status_code != 200:
            print("Could not reach update server.")
            return

        remote_version = response.text.strip()
        local_version = get_local_version()

        if remote_version != local_version:
            print(f"New version found: {remote_version} (Local: {local_version})")
            
            # 2. Download Files
            for filename in FILES_TO_UPDATE:
                print(f"Updating {filename}...")
                file_resp = requests.get(GITHUB_RAW_URL + filename, timeout=10)
                if file_resp.status_code == 200:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(file_resp.text)
                else:
                    print(f"Failed to download {filename}")
            
            # 3. Update local version file
            with open(VERSION_FILE, "w") as f:
                f.write(remote_version)
            
            print("Update complete!")
        else:
            print("App is up to date.")
            
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    update()
