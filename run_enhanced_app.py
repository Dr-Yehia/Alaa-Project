#!/usr/bin/env python3
"""
Enhanced launcher for the Monorail LCA/LCCA Assessment Tool
This script provides a user-friendly way to launch the enhanced application
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import numpy
        print("✓ NumPy available")
    except ImportError:
        missing_deps.append("numpy")
        print("✗ NumPy not found")
    
    try:
        import matplotlib
        print("✓ Matplotlib available")
    except ImportError:
        missing_deps.append("matplotlib")
        print("✗ Matplotlib not found")
    
    try:
        import pandas
        print("✓ Pandas available")
    except ImportError:
        missing_deps.append("pandas")
        print("✗ Pandas not found")
    
    try:
        import tkinter
        print("✓ Tkinter available")
    except ImportError:
        missing_deps.append("tkinter")
        print("✗ Tkinter not found")
    
    try:
        import openpyxl
        print("✓ OpenPyXL available (for Excel export)")
    except ImportError:
        missing_deps.append("openpyxl")
        print("✗ OpenPyXL not found (Excel export will not work)")
    
    return missing_deps

def install_dependencies():
    """Provide instructions for installing missing dependencies"""
    print("\n" + "="*60)
    print("MISSING DEPENDENCIES DETECTED")
    print("="*60)
    print("Please install the missing packages using pip:")
    print("\npip install numpy matplotlib pandas openpyxl")
    print("\nOr install all requirements:")
    print("pip install -r requirements.txt")
    print("\n" + "="*60)

def main():
    """Main launcher function"""
    print("Enhanced Monorail LCA/LCCA Assessment Tool")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return 1
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check dependencies
    print("\nChecking dependencies...")
    missing_deps = check_dependencies()
    
    if missing_deps:
        install_dependencies()
        return 1
    
    # Try to import the main application
    try:
        print("\nLoading enhanced application...")
        from SD_LCA_LCCA_Enhanced import main as app_main
        print("✓ Enhanced application loaded successfully")
        
        # Launch the application
        print("\n🚀 Launching Enhanced Monorail LCA/LCCA Assessment Tool...")
        print("=" * 60)
        print("New Features:")
        print("• Input validation and error handling")
        print("• Export to Excel/CSV functionality")
        print("• Scientific methodology documentation")
        print("• Enhanced user interface with tabs")
        print("• Comprehensive reporting capabilities")
        print("=" * 60)
        app_main()
        
    except ImportError as e:
        print(f"❌ Error importing enhanced application: {e}")
        print("\nMake sure SD_LCA_LCCA_Enhanced.py is in the same directory")
        return 1
    
    except Exception as e:
        print(f"❌ Error launching enhanced application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 