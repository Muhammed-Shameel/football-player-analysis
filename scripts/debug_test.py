import requests
import json

# Test the get_managers_for_player endpoint
url = 'http://localhost:5000/get_managers_for_player'
data = {
    'player_id': 'P01',
    'model_name': 'XGBoost'
}

try:
    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
    response_data = response.json()
    print("Full Response:", json.dumps(response_data, indent=2))
    
    # Check the recommended managers
    managers = response_data.get('recommended_managers', [])
    print("\nRecommended Managers:")
    for manager in managers:
        print(f"  ID: {manager.get('Manager_ID')}")
        print(f"  Name: {manager.get('Manager_Name')}")
        print(f"  Score: {manager.get('relevance_score')}")
        print(f"  Formations: {manager.get('formations')}")
        print()
        
except Exception as e:
    print("Error:", str(e))