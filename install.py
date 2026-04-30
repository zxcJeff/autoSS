import os
import time
import subprocess
import sys

def installPipreqs():
    try:
        import pipreqs
        import openpyxl
    except ImportError:
        print("Installing missing dependencies: pipreqs, openpyxl...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pipreqs", "openpyxl"], check=True)
        print("Dependencies installed successfully.")
        time.sleep(1)

def generateRequirements():
    if not any(f.endswith(".py") for f in os.listdir(".")):
        print("No Python files found. Skipping requirements generation.")
        return False
    
    try:
        subprocess.run(["pipreqs", ".", "--force"], check=True)
        print("requirements.txt generated successfully.")
        time.sleep(1)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while generating requirements.txt: {e}")
        return False

def installModules():
    try:
        installPipreqs()
        
        if not generateRequirements():
            print("Failed to generate requirements.txt. Exiting.")
            return
        
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        
        os.system("cls" if os.name == "nt" else "clear")
        print("All requirements installed successfully.")
        time.sleep(2)
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing requirements: {e}")

installModules()
