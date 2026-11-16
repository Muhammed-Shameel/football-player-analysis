import requests
import json

# Test the get_recommendations endpoint
url = 'http://localhost:5000/get_recommendations'
data = {
    'player_id': 'P01',
    'model_name': 'XGBoost'
}

try:
    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
    response_data = response.json()
    print("Response keys:", response_data.keys())
    print("Recommended managers:", response_data.get('recommended_managers', []))
except Exception as e:
    print("Error:", str(e))