import subprocess
import os
import sys
import webbrowser
import time
import ctypes

def is_frozen():
    return getattr(sys, 'frozen', False)

def show_error(title, message):
    if os.name == 'nt':
        ctypes.windll.user32.MessageBoxW(0, message, title, 16) # 16 = MB_ICONERROR
    else:
        print(f"ERROR: {title}\n{message}")

def launch():
    # 1. Determine paths
    if is_frozen():
        base_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    python_exe = os.path.join(base_path, "python_bin", "python.exe")
    
    if not os.path.exists(python_exe):
        if not is_frozen():
            python_exe = sys.executable
        else:
            show_error("Startup Error", f"Portable engine missing at:\n{python_exe}\n\nPlease ensure 'python_bin' is in the same folder as this EXE.")
            return

    # Safety: Recursion check
    if is_frozen() and os.path.abspath(python_exe) == os.path.abspath(sys.executable):
        show_error("Recursion Error", "The launcher attempted to call itself as an engine. Aborting.")
        return

    # 2. Run Update Engine
    print("Checking for updates...")
    try:
        subprocess.run([python_exe, "updater.py"], cwd=base_path, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
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
    
    log_path = os.path.join(base_path, "latest_launch_log.txt")
    try:
        with open(log_path, "w") as log_file:
            subprocess.Popen(
                cmd, 
                cwd=base_path, 
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                stdout=log_file,
                stderr=log_file
            )
    except Exception as e:
        show_error("Launch Error", f"Failed to start Streamlit: {e}")
        return

    # 4. Manually open browser
    print("Opening browser...")
    time.sleep(4)
    webbrowser.open("http://localhost:8501")
    print("Process complete. You can close this window.")

if __name__ == "__main__":
    launch()
