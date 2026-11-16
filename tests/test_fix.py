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
    print("Response:", response.json())
except Exception as e:
    print("Error:", str(e))