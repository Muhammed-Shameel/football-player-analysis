import requests
import json

# Test the player info endpoint
print("Testing /get_player_info endpoint...")
try:
    response = requests.get('http://localhost:5000/get_player_info?player_id=P01&year=2023')
    if response.status_code == 200:
        data = response.json()
        print("Player info response:", json.dumps(data, indent=2))
        print("✅ Player info endpoint working correctly")
    else:
        print(f"❌ Player info endpoint failed with status {response.status_code}")
except Exception as e:
    print(f"❌ Player info endpoint error: {e}")

# Test the recommendations endpoint
print("\nTesting /get_recommendations endpoint...")
try:
    response = requests.post('http://localhost:5000/get_recommendations', 
                           data={'player_id': 'P01', 'year': 2023})
    if response.status_code == 200:
        data = response.json()
        print("Recommendations response keys:", list(data.keys()))
        if 'scores' in data and data['scores']:
            print("✅ Scores data included in recommendations")
            print("Scores:", data['scores'])
        else:
            print("❌ Scores data missing from recommendations")
        if 'best_component' in data:
            print("✅ Best component included in recommendations")
        else:
            print("❌ Best component missing from recommendations")
    else:
        print(f"❌ Recommendations endpoint failed with status {response.status_code}")
except Exception as e:
    print(f"❌ Recommendations endpoint error: {e}")