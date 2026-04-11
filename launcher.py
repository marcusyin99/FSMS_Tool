import subprocess
import os
import sys
import webbrowser
import time

def launch():
    # 1. Determine paths
    root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    internal_path = os.path.join(root_path, "Internal_Files")
    
    python_exe = os.path.join(internal_path, "python_bin", "python.exe")
    
    if not os.path.exists(python_exe):
        python_exe = sys.executable

    # IMPORTANT: Change working directory to Internal_Files so all scripts work correctly
    os.chdir(internal_path)

    # 2. Run Update Engine
    print("Checking for updates...")
    try:
        subprocess.run([python_exe, "updater.py"], timeout=30)
    except Exception as e:
        print(f"Update check skipped: {e}")

    # 3. Launch Streamlit
    print("Launching Company Toolbelt...")
    cmd = [
        python_exe, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--global.developmentMode", "false"
    ]
    
    # Logs are now stored inside Internal_Files
    log_path = os.path.join(internal_path, "latest_launch_log.txt")
    with open(log_path, "w") as log_file:
        proc = subprocess.Popen(
            cmd, 
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
            stdout=log_file,
            stderr=log_file
        )

    # 4. Manually open browser
    print("Opening browser...")
    time.sleep(3)
    webbrowser.open("http://localhost:8501")
    print("Process complete. You can close this window.")

if __name__ == "__main__":
    launch()
