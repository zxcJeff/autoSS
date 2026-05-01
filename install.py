import os
import time
import subprocess
import sys

def progress_bar(current, total, bar_length=40, prefix="Progress:"):
    """Display a progress bar"""
    fraction = current / total
    arrow = '=' * int(round(fraction * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    
    percent = int(round(fraction * 100))
    
    # Format the progress bar
    bar = f"[{arrow}{spaces}] {percent}%"
    
    # Add prefix and ensure it updates on the same line
    sys.stdout.write(f'\r{prefix} {bar}')
    sys.stdout.flush()

def installPipreqs():
    """Check and install required dependencies"""
    missing_packages = []
    
    print("\n📦 Checking base dependencies...")
    
    try:
        import pipreqs
        print("  ✓ pipreqs found")
    except ImportError:
        missing_packages.append("pipreqs")
        print("  ✗ pipreqs missing")
    
    try:
        import openpyxl
        print("  ✓ openpyxl found")
    except ImportError:
        missing_packages.append("openpyxl")
        print("  ✗ openpyxl missing")
    
    if missing_packages:
        print(f"\n📥 Installing missing dependencies: {', '.join(missing_packages)}...")
        
        for i, package in enumerate(missing_packages):
            progress_bar(i + 1, len(missing_packages), prefix=f"Installing {package}:")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              check=True, capture_output=True, text=True)
                time.sleep(0.5)
            except subprocess.CalledProcessError as e:
                print(f"\n❌ Error installing {package}: {e.stderr}")
                return False
        
        print("\n✅ Dependencies installed successfully.")
        time.sleep(1)
        return True
    else:
        print("\n✅ All required dependencies already installed.")
        return True

def generateRequirements():
    """Generate requirements.txt from Python files"""
    python_files = [f for f in os.listdir(".") if f.endswith(".py")]
    
    if not python_files:
        print("❌ No Python files found. Skipping requirements generation.")
        return False
    
    print(f"\n📁 Found {len(python_files)} Python files:")
    for py_file in python_files:
        print(f"  - {py_file}")
    
    print("\n📝 Generating requirements.txt...")
    
    # Progress bar for generation process
    progress_bar(1, 4, prefix="Scanning imports:")
    time.sleep(0.5)
    
    try:
        # Use --savepath to specify output location
        result = subprocess.run(
            ["pipreqs", ".", "--force", "--encoding=utf-8"], 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        progress_bar(3, 4, prefix="Creating requirements.txt:")
        time.sleep(0.5)
        progress_bar(4, 4, prefix="Complete:")
        time.sleep(0.5)
        
        print("\n✅ requirements.txt generated successfully.")
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        time.sleep(1)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error generating requirements.txt: {e.stderr}")
        return False
    except FileNotFoundError:
        print("\n❌ pipreqs command not found. Please ensure pipreqs is installed correctly.")
        return False

def installPackagesFromRequirements():
    """Install packages from requirements.txt with progress bar"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found.")
        return False
    
    # Count packages in requirements.txt
    with open("requirements.txt", "r") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not packages:
        print("⚠️  requirements.txt is empty.")
        return False
    
    print(f"\n📦 Found {len(packages)} packages to install:")
    for pkg in packages[:5]:  # Show first 5
        print(f"  - {pkg}")
    if len(packages) > 5:
        print(f"  ... and {len(packages) - 5} more")
    
    print("\n🚀 Installing packages...")
    
    # Install with progress bar
    for i, package in enumerate(packages):
        progress_bar(i + 1, len(packages), prefix=f"Installing packages ({i+1}/{len(packages)}):")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "--quiet"],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"\n⚠️  Warning: Failed to install {package}")
            if e.stderr:
                print(f"   Error: {e.stderr[:100]}...")
    
    print("\n✅ All packages installed successfully!")
    time.sleep(1)
    return True

def installPlaywright():
    """Install Playwright browsers with progress bar"""
    print("\n🎭 Installing Playwright browsers...")
    
    steps = [
        "Installing playwright package",
        "Downloading Firefox browser",
        "Installing Firefox dependencies",
        "Finalizing installation"
    ]
    
    for i, step in enumerate(steps):
        progress_bar(i + 1, len(steps), prefix=step)
        time.sleep(0.8)  # Simulate progress for visual effect
        
        if i == 0:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "--quiet"],
                             check=True, capture_output=True, text=True)
            except:
                pass
        elif i == 1:
            try:
                subprocess.run([sys.executable, "-m", "playwright", "install", "firefox"],
                             check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"\n❌ Error installing Playwright: {e.stderr}")
                return False
            except FileNotFoundError:
                print("\n⚠️  Playwright not found. Installing playwright first...")
                subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "--quiet"],
                             check=True)
                subprocess.run([sys.executable, "-m", "playwright", "install", "firefox"],
                             check=True)
    
    print("\n✅ Playwright browsers installed successfully!")
    time.sleep(1)
    return True

def installModules():
    """Main function to install all requirements"""
    os.system("cls" if os.name == "nt" else "clear")
    
    print("=" * 60)
    print("           AutoSS Dependency Installer")
    print("=" * 60)
    
    total_steps = 4
    current_step = 0
    
    # Step 1: Install pipreqs and openpyxl
    current_step += 1
    print(f"\n{'='*60}")
    print(f"STEP {current_step}/{total_steps}: Checking Base Dependencies")
    print(f"{'='*60}")
    
    if not installPipreqs():
        print("\n❌ Failed to install base dependencies. Exiting.")
        input("\nPress Enter to exit...")
        return
    
    # Step 2: Generate requirements.txt
    current_step += 1
    print(f"\n{'='*60}")
    print(f"STEP {current_step}/{total_steps}: Generating requirements.txt")
    print(f"{'='*60}")
    
    if not generateRequirements():
        print("\n❌ Failed to generate requirements.txt. Exiting.")
        input("\nPress Enter to exit...")
        return
    
    # Step 3: Install packages from requirements.txt
    current_step += 1
    print(f"\n{'='*60}")
    print(f"STEP {current_step}/{total_steps}: Installing Python Packages")
    print(f"{'='*60}")
    
    if not installPackagesFromRequirements():
        print("\n⚠️  Failed to install from requirements.txt")
        print("📦 Attempting to install common packages manually...")
        
        common_packages = ["requests", "pandas", "openpyxl", "colorama", "playwright"]
        print(f"\n📥 Installing {len(common_packages)} common packages...")
        
        for i, package in enumerate(common_packages):
            progress_bar(i + 1, len(common_packages), prefix=f"Installing {package}:")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package, "--quiet"], 
                             check=True, capture_output=True, text=True)
                time.sleep(0.3)
            except:
                pass
        
        print("\n✅ Common packages installed!")
    
    # Step 4: Install Playwright browsers
    current_step += 1
    print(f"\n{'='*60}")
    print(f"STEP {current_step}/{total_steps}: Installing Playwright Browsers")
    print(f"{'='*60}")
    
    installPlaywright()
    
    # Success message with animation
    os.system("cls" if os.name == "nt" else "clear")
    
    print("\n" + "=" * 60)
    print("                     ✓ SUCCESS! ✓")
    print("=" * 60)
    print("\n   All requirements have been installed successfully!")
    print("\n   You can now run the application:")
    print("   python main.py")
    print("\n" + "=" * 60)
    
    # Countdown to exit
    print("\nClosing in", end="")
    for i in range(5, 0, -1):
        print(f" {i}...", end="", flush=True)
        time.sleep(1)
    print("\n")

if __name__ == "__main__":
    try:
        installModules()
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)