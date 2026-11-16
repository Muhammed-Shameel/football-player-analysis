#!/usr/bin/env python3
"""
Test script to verify that the Flask app can be imported without errors
"""

def test_app_import():
    """Test importing the main app"""
    try:
        import app_simple
        print("✅ app_simple.py imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import app_simple.py: {e}")
        return False

def test_flask_import():
    """Test importing Flask"""
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import Flask: {e}")
        return False

def test_pandas_import():
    """Test importing pandas"""
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import Pandas: {e}")
        return False

def test_numpy_import():
    """Test importing numpy"""
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import NumPy: {e}")
        return False

def main():
    print("Testing imports for Football Tactical Recommendations Dashboard")
    print("=" * 60)
    
    tests = [
        test_flask_import,
        test_pandas_import,
        test_numpy_import,
        test_app_import
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    if all(results):
        print("🎉 All imports successful!")
        print("You can now run the application with: python app_simple.py")
    else:
        print("❌ Some imports failed. Please check the errors above.")

if __name__ == "__main__":
    main()