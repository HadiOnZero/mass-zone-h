#!/usr/bin/env python3
"""
Setup script for Zone-H Mass Mirror Tool
This script helps with installation and setup of the application
Author: Hadi Ramdhani
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        if os.path.exists("requirements.txt"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ All packages installed successfully!")
            return True
        else:
            print("❌ requirements.txt not found!")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "PyQt5",
        "requests",
        "beautifulsoup4",
        "lxml"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - NOT INSTALLED")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def create_desktop_shortcut():
    """Create desktop shortcut (optional)"""
    print("\n📝 Creating desktop shortcut...")
    
    try:
        desktop_path = Path.home() / "Desktop"
        if platform.system() == "Windows":
            desktop_path = Path.home() / "Desktop"
            shortcut_content = f"""@echo off
cd /d "{os.getcwd()}"
python main.py
pause
"""
            shortcut_file = desktop_path / "Zone-H Mirror.bat"
            with open(shortcut_file, 'w') as f:
                f.write(shortcut_content)
                
        elif platform.system() == "Darwin":  # macOS
            desktop_path = Path.home() / "Desktop"
            shortcut_content = f"""#!/bin/bash
cd "{os.getcwd()}"
python3 main.py
"""
            shortcut_file = desktop_path / "Zone-H Mirror.command"
            with open(shortcut_file, 'w') as f:
                f.write(shortcut_content)
            os.chmod(shortcut_file, 0o755)
            
        else:  # Linux
            desktop_path = Path.home() / "Desktop"
            shortcut_content = f"""#!/bin/bash
cd "{os.getcwd()}"
python3 main.py
"""
            shortcut_file = desktop_path / "Zone-H Mirror.sh"
            with open(shortcut_file, 'w') as f:
                f.write(shortcut_content)
            os.chmod(shortcut_file, 0o755)
        
        print(f"✅ Desktop shortcut created: {shortcut_file}")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")
        return False

def make_launcher_executable():
    """Make launcher scripts executable"""
    print("\n🔧 Setting up launcher scripts...")
    
    try:
        if platform.system() != "Windows":
            # Make shell scripts executable
            if os.path.exists("run.sh"):
                os.chmod("run.sh", 0o755)
                print("✅ run.sh is now executable")
            
            if os.path.exists("setup.py"):
                os.chmod("setup.py", 0o755)
                print("✅ setup.py is now executable")
        
        print("✅ Launcher scripts configured!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up launcher scripts: {e}")
        return False

def main():
    """Main setup function"""
    print("🎯 Zone-H Mass Mirror Tool - Setup")
    print("=" * 40)
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    print()
    
    # Install requirements
    if not install_requirements():
        return False
    
    print()
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    print()
    
    # Make launcher scripts executable
    make_launcher_executable()
    
    print()
    
    # Create desktop shortcut (optional)
    create_desktop_shortcut()
    
    print()
    print("🎉 Setup completed successfully!")
    print("You can now run the application using:")
    print("  - python main.py")
    print("  - ./run.sh (Linux/Mac)")
    print("  - run.bat (Windows)")
    print()
    print("📖 For more information, check README.md")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)