import requests
import time

# Test the dashboard endpoints
def test_dashboard():
    base_url = "http://127.0.0.1:5000"
    
    print("Testing Football Tactical Recommendations Dashboard...")
    
    # Test main page
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✓ Main dashboard page loads successfully")
        else:
            print(f"✗ Main dashboard page failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Failed to load main dashboard page: {e}")
    
    # Test player info endpoint (using first player ID from player.xlsx)
    try:
        response = requests.get(f"{base_url}/get_player_info?player_id=P01")
        if response.status_code == 200:
            data = response.json()
            print("✓ Player info endpoint works correctly")
            print(f"  Player name: {data.get('Common_Name', 'N/A')}")
        else:
            print(f"✗ Player info endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Failed to get player info: {e}")
    
    # Test recommendations endpoint
    try:
        form_data = {
            'player_id': 'P01',
            'model_name': 'XGBoost'
        }
        response = requests.post(f"{base_url}/get_recommendations", data=form_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ Tactical recommendations endpoint works correctly")
            if 'recommendations' in data:
                print(f"  Number of recommendations: {len(data['recommendations'])}")
                best_component = data.get('best_component', {})
                if best_component:
                    print(f"  Best tactic component: {best_component.get('component', 'N/A')}")
                    print(f"  Best tactic value: {best_component.get('value', 'N/A')}")
            else:
                print("  No recommendations found")
        else:
            print(f"✗ Tactical recommendations endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Failed to get tactical recommendations: {e}")

if __name__ == "__main__":
    test_dashboard()