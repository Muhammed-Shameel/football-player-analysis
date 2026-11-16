import requests
import json
import time

# Test the Flask app endpoints
def test_app():
    base_url = 'http://localhost:5000'
    
    # Test 1: Check if the main page loads
    try:
        response = requests.get(base_url + '/')
        print(f"Test 1 - Main page status code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Main page loads successfully")
        else:
            print("✗ Main page failed to load")
    except Exception as e:
        print(f"✗ Error accessing main page: {e}")
    
    # Test 2: Check if the managers page loads
    try:
        response = requests.get(base_url + '/managers')
        print(f"Test 2 - Managers page status code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Managers page loads successfully")
        else:
            print("✗ Managers page failed to load")
    except Exception as e:
        print(f"✗ Error accessing managers page: {e}")
    
    # Test 3: Check if the insights page loads
    try:
        response = requests.get(base_url + '/insights')
        print(f"Test 3 - Insights page status code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Insights page loads successfully")
        else:
            print("✗ Insights page failed to load")
    except Exception as e:
        print(f"✗ Error accessing insights page: {e}")
    
    # Test 4: Check API endpoints with sample data
    try:
        # Test get_manager_summary endpoint
        response = requests.get(base_url + '/get_manager_summary')
        print(f"Test 4 - Manager summary API status code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Manager summary API works")
            try:
                data = response.json()
                print(f"  Number of managers: {len(data)}")
            except:
                print("  Could not parse JSON response")
        else:
            print("✗ Manager summary API failed")
    except Exception as e:
        print(f"✗ Error accessing manager summary API: {e}")

if __name__ == "__main__":
    print("Testing Flask app...")
    test_app()
    print("Test completed.")