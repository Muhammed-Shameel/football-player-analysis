import sys
import importlib

# List of required packages
required_packages = [
    'flask',
    'pandas',
    'numpy',
    'pickle',
    'json',
    'collections',
    'datetime',
    'calendar',
    'warnings',
    'os',
    'random'
]

# Additional packages that might be needed
optional_packages = [
    'openpyxl',  # for reading Excel files
    'sklearn'    # for machine learning models
]

def check_package(package_name):
    """Check if a package can be imported"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def main():
    print("Checking required packages for the Football Tactical Recommendations Dashboard...")
    print("=" * 80)
    
    # Check required packages
    print("Required packages:")
    all_required_found = True
    for package in required_packages:
        if check_package(package):
            print(f"  ✓ {package}")
        else:
            print(f"  ✗ {package} (MISSING)")
            all_required_found = False
    
    print("\nOptional packages:")
    for package in optional_packages:
        if check_package(package):
            print(f"  ✓ {package}")
        else:
            print(f"  ✗ {package} (MISSING - but not critical)")
    
    print("\n" + "=" * 80)
    if all_required_found:
        print("✓ All required packages are available!")
        print("You can now run the app with: python app.py")
    else:
        print("✗ Some required packages are missing!")
        print("Please install the missing packages before running the app.")
        
        # Check if we're in the right environment
        print(f"\nCurrent Python version: {sys.version}")
        print("Make sure you're running this in an environment with the required packages.")

if __name__ == "__main__":
    main()