import requests
import json

# Test the get_manager_analysis endpoint
url = 'http://localhost:5000/get_manager_analysis'
params = {
    'manager_id': 'M01',
    'model': 'XGBoost'
}

try:
    response = requests.get(url, params=params)
    print("Status code:", response.status_code)
    print("Response headers:", response.headers)
    
    if response.status_code == 200:
        data = response.json()
        print("Response data keys:", data.keys())
        print("Manager info:", data.get('manager_info'))
        print("Number of top players:", len(data.get('top_players', [])))
        if data.get('top_players'):
            print("First player:", data['top_players'][0])
        print("Formations:", data.get('formations'))
        print("Insights:", data.get('insights'))
    else:
        print("Error response:", response.text)
        
except Exception as e:
    print("Error making request:", str(e))
    import traceback
    traceback.print_exc()