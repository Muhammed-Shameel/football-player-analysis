import requests
import json

# Test all the main endpoints to verify the fixes
base_url = 'http://localhost:5000'

print("Testing the Capstone Project Flask App")
print("=" * 50)

# Test 1: Get player info
print("\n1. Testing /get_player_info endpoint...")
try:
    response = requests.get(f"{base_url}/get_player_info?player_id=P01")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Player Name: {data.get('Common_Name', 'N/A')}")
        print(f"   Success: Player info endpoint working correctly")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 2: Get recommendations
print("\n2. Testing /get_recommendations endpoint...")
try:
    response = requests.post(f"{base_url}/get_recommendations", data={'player_id': 'P01', 'model_name': 'XGBoost'})
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Best Component: {data.get('best_component', {}).get('component', 'N/A')}")
        managers = data.get('recommended_managers', [])
        print(f"   Number of Recommended Managers: {len(managers)}")
        if managers:
            print(f"   First Manager: {managers[0].get('Manager_Name', 'N/A')} (Score: {managers[0].get('relevance_score', 'N/A')})")
            print(f"   First Manager Formations: {managers[0].get('formations', 'N/A')}")
        print(f"   Success: Recommendations endpoint working correctly")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 3: Get managers for player
print("\n3. Testing /get_managers_for_player endpoint...")
try:
    response = requests.post(f"{base_url}/get_managers_for_player", data={'player_id': 'P01', 'model_name': 'XGBoost'})
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        managers = data.get('recommended_managers', [])
        print(f"   Number of Recommended Managers: {len(managers)}")
        if managers:
            print(f"   First Manager: {managers[0].get('Manager_Name', 'N/A')} (Score: {managers[0].get('relevance_score', 'N/A')})")
            print(f"   First Manager Formations: {managers[0].get('formations', 'N/A')}")
        print(f"   Success: Managers for player endpoint working correctly")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {str(e)}")

print("\n" + "=" * 50)
print("Testing completed.")