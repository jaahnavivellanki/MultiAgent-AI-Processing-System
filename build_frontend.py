import os
import subprocess
import shutil
import sys
import os.path

def check_node_installation():
    try:
        # Get the system PATH
        system_path = os.environ.get('PATH', '')
        
        # Try to find node and npm in common installation directories
        common_paths = [
            r'C:\Program Files\nodejs',
            r'C:\Program Files (x86)\nodejs',
            os.path.expanduser('~\\AppData\\Roaming\\npm'),
            os.path.expanduser('~\\AppData\\Local\\Programs\\nodejs')
        ]
        
        # Add common paths to PATH temporarily
        os.environ['PATH'] = system_path + os.pathsep + os.pathsep.join(common_paths)
        
        # Try to run node and npm directly
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
        print(f"Error checking Node.js installation: {str(e)}")
        return False

def build_frontend():
    print("Building frontend application...")
    
    # Check for Node.js installation
    if not check_node_installation():
        print("\nTrying to continue with build process anyway...")
    
    # Check if frontend directory exists
    if not os.path.exists("frontend"):
        print("Error: frontend directory not found!")
        print("Please make sure you're running this script from the project root directory.")
        sys.exit(1)
    
    # Change to frontend directory
    os.chdir("frontend")
    
    try:
        # Install dependencies if node_modules doesn't exist
        if not os.path.exists("node_modules"):
            print("Installing dependencies...")
            subprocess.run("npm install", shell=True, check=True)
        
        # Build the frontend
        print("Building React application...")
        subprocess.run("npm run build", shell=True, check=True)
        
        print("Frontend build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        # Move back to root directory
        os.chdir("..")

if __name__ == "__main__":
    build_frontend() 