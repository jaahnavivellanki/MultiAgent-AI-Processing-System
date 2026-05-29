import subprocess
import sys
import os
import webbrowser
from time import sleep

def check_requirements():
    """Check if all required software is installed."""
    try:
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
            print("Error: Python 3.7 or higher is required.")
            return False

        # Check Node.js installation
        try:
            node_version = subprocess.check_output('node --version', shell=True).decode().strip()
            npm_version = subprocess.check_output('npm --version', shell=True).decode().strip()
            print(f"Found Node.js version: {node_version}")
            print(f"Found npm version: {npm_version}")
            return True
        except subprocess.CalledProcessError:
            print("Could not execute node or npm commands")
            return False

    except Exception as e:
        print(f"Error checking requirements: {str(e)}")
        return False

def run_application():
    # Check requirements first
    if not check_requirements():
        print("\nTrying to continue anyway...")

    try:
        # Build the frontend first
        print("Building frontend...")
        subprocess.run("py build_frontend.py", shell=True, check=True)
        
        # Start the backend server
        print("Starting backend server...")
        backend_process = subprocess.Popen("py server.py", shell=True)
        
        # Wait a moment for the server to start
        sleep(2)
        
        # Open the browser
        print("Opening application in browser...")
        webbrowser.open("http://localhost:8000")
        
        try:
            # Keep the script running
            backend_process.wait()
        except KeyboardInterrupt:
            print("\nShutting down...")
            backend_process.terminate()
            backend_process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Error during application startup: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_application() 