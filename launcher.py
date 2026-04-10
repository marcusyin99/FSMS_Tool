import subprocess
import os
import sys
import updater

def main():
    # 1. Execute the update logic natively before locking Streamlit resources
    try:
        updater.check_and_update()
    except Exception as e:
        print(f"Bypassing updater due to error: {e}")
        
    # 2. Map coordinates for the portable environment
    portable_python = os.path.join(os.getcwd(), "python_portable", "python.exe")
    app_script = os.path.join(os.getcwd(), "app.py")
    
    # 3. Suppress all child terminal popups
    creationflags = 0x08000000 if os.name == 'nt' else 0
    
    if not os.path.exists(portable_python):
        print("CRITICAL WARNING: Portable Python not found. Initiating System Python globally.")
        portable_python = "python"
        
    print("Launching Streamlit Application invisibly...")
    
    subprocess.Popen(
        [portable_python, "-m", "streamlit", "run", app_script], 
        creationflags=creationflags
    )

if __name__ == "__main__":
    main()
