#!/usr/bin/env python3
"""
Verification script for the Football Tactical Recommendations Dashboard
This script checks if the application can start and if all required files are present.
"""

import os
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        return False
    print("✅ Python version is compatible")
    return True

def check_required_files():
    """Check if all required files are present"""
    required_files = [
        'player.xlsx',
        'df_model.csv',
        'team.xlsx',
        'manager.xlsx',
        'manager_formation.xlsx',
        'manager_tactics.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ Found {file}")
    
    if missing_files:
        print(f"⚠ Missing files: {', '.join(missing_files)}")
        print("  The app will still run but with limited functionality")
        return False
    else:
        print("✅ All required data files are present")
        return True

def check_templates():
    """Check if template files are present"""
    template_dir = 'templates'
    required_templates = [
        'index.html',
        'managers.html',
        'insights.html'
    ]
    
    if not os.path.exists(template_dir):
        print("❌ templates directory not found")
        return False
    
    missing_templates = []
    for template in required_templates:
        template_path = os.path.join(template_dir, template)
        if not os.path.exists(template_path):
            missing_templates.append(template)
        else:
            print(f"✅ Found {template}")
    
    if missing_templates:
        print(f"❌ Missing templates: {', '.join(missing_templates)}")
        return False
    else:
        print("✅ All required templates are present")
        return True

def check_static_files():
    """Check if static directory structure is correct"""
    static_dir = 'static'
    images_dir = os.path.join(static_dir, 'images')
    
    if not os.path.exists(static_dir):
        print("❌ static directory not found")
        return False
    
    print("✅ Found static directory")
    
    if not os.path.exists(images_dir):
        print("⚠ static/images directory not found")
        print("  Player images will not be displayed")
    else:
        print("✅ Found static/images directory")
    
    return True

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask',
        'pandas',
        'numpy',
        'openpyxl'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is not installed")
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("  Install them with: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✅ All required packages are installed")
        return True

def main():
    print("Football Tactical Recommendations Dashboard - Verification")
    print("=" * 60)
    
    # Run all checks
    checks = [
        check_python_version,
        check_dependencies,
        check_required_files,
        check_templates,
        check_static_files
    ]
    
    results = []
    for check in checks:
        print(f"\nChecking {check.__name__}...")
        results.append(check())
    
    print("\n" + "=" * 60)
    if all(results):
        print("🎉 All checks passed! You can now run the application:")
        print("   python app_simple.py")
    else:
        print("⚠ Some checks failed. Please address the issues above.")
        print("   The application may still run with limited functionality.")

if __name__ == "__main__":
    main()