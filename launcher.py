import subprocess
import os
import sys
import webbrowser
import time

def launch():
    # 1. Determine paths
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    python_exe = os.path.join(base_path, "python_bin", "python.exe")
    
    if not os.path.exists(python_exe):
        python_exe = sys.executable

    # 2. Run Update Engine
    print("Checking for updates...")
    try:
        subprocess.run([python_exe, "updater.py"], cwd=base_path, timeout=30)
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
    
    # We redirect output to a log file so we can see if it crashes
    log_path = os.path.join(base_path, "latest_launch_log.txt")
    with open(log_path, "w") as log_file:
        proc = subprocess.Popen(
            cmd, 
            cwd=base_path, 
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
            stdout=log_file,
            stderr=log_file
        )

    # 4. Manually open browser after a short delay to let server start
    print("Opening browser...")
    time.sleep(3)
    webbrowser.open("http://localhost:8501")
    print("Process complete. You can close this window.")

if __name__ == "__main__":
    launch()
