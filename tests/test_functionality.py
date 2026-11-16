import requests
import json

# Test the main functionality
def test_app():
    base_url = 'http://127.0.0.1:5000'
    
    print("Testing Flask app functionality...")
    
    # Test 1: Check if main page loads
    try:
        response = requests.get(f'{base_url}/')
        print(f"✓ Main page status: {response.status_code}")
    except Exception as e:
        print(f"✗ Main page error: {e}")
    
    # Test 2: Check insights page
    try:
        response = requests.get(f'{base_url}/insights')
        print(f"✓ Insights page status: {response.status_code}")
    except Exception as e:
        print(f"✗ Insights page error: {e}")
    
    # Test 3: Check tactical components page
    try:
        response = requests.get(f'{base_url}/tactical_components')
        print(f"✓ Tactical components page status: {response.status_code}")
    except Exception as e:
        print(f"✗ Tactical components page error: {e}")
    
    # Test 4: Test player info endpoint
    try:
        response = requests.get(f'{base_url}/get_player_info?player_id=P01')
        data = response.json()
        print(f"✓ Player info endpoint status: {response.status_code}")
        print(f"  Player name: {data.get('Common_Name', 'N/A')}")
        print(f"  Impact score: {data.get('Impact_Score', 'N/A')}")
    except Exception as e:
        print(f"✗ Player info endpoint error: {e}")
    
    # Test 5: Test recommendations endpoint
    try:
        response = requests.post(f'{base_url}/get_recommendations', data={
            'player_id': 'P01',
            'model_name': 'XGBoost'
        })
        data = response.json()
        print(f"✓ Recommendations endpoint status: {response.status_code}")
        if 'best_component' in data:
            print(f"  Best tactic: {data['best_component']['component']}")
            print(f"  Value: {data['best_component']['value']:.2f}")
    except Exception as e:
        print(f"✗ Recommendations endpoint error: {e}")
    
    # Test 6: Test impact over time endpoint
    try:
        response = requests.get(f'{base_url}/get_impact_over_time?player_id=P01')
        data = response.json()
        print(f"✓ Impact over time endpoint status: {response.status_code}")
        impact_data = data.get('impact_over_time', [])
        print(f"  Impact data points: {len(impact_data)}")
    except Exception as e:
        print(f"✗ Impact over time endpoint error: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_app()