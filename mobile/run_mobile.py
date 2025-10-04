#!/usr/bin/env python3
"""
Launcher script for Zone-H Mobile Mirror Application
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main_mobile import main
    
    if __name__ == '__main__':
        print("🚀 Starting Zone-H Mobile Mirror Application...")
        print("📱 Mobile version with Kivy framework")
        print("=" * 50)
        main()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies:")
    print("pip install -r requirements_mobile.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Application error: {e}")
    sys.exit(1)