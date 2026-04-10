import requests
import os

def check_and_update():
    try:
        with open("version.txt", "r") as f:
            local_version = f.read().strip()
    except FileNotFoundError:
        local_version = "1.0.0"
        
    print(f"Checking for updates. Local version: {local_version}")
    url = "https://raw.githubusercontent.com/marcusyin99/FSMS_Tool/main/version.json"
    
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            remote_data = resp.json()
            remote_version = remote_data.get("version", "0.0.0")
            files_to_update = remote_data.get("files", [])
            
            if remote_version > local_version:
                print(f"Update Available! Version {remote_version}. Downloading...")
                for filename in files_to_update:
                    file_url = f"https://raw.githubusercontent.com/marcusyin99/FSMS_Tool/main/{filename}"
                    file_resp = requests.get(file_url, timeout=10)
                    file_resp.raise_for_status()
                    
                    with open(filename, "wb") as f:
                        f.write(file_resp.content)
                        
                with open("version.txt", "w") as f:
                    f.write(remote_version)
                print("Update successfully installed!")
            else:
                print("You are on the latest version.")
        else:
            print("Could not reach update server.")
    except Exception as e:
        print(f"Update check failed/Offline mode active: {e}")

if __name__ == "__main__":
    check_and_update()
