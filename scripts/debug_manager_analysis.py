import pandas as pd
import json
from app import get_top_players_for_manager, get_manager_name

# Load data
df_model = pd.read_csv('df_model.csv')
print("df_model loaded successfully, shape:", df_model.shape)

with open('manager_tactics.json', 'r') as f:
    manager_tactics = json.load(f)
print("manager_tactics loaded successfully")

# Test with a specific manager
manager_id = 'M01'
print(f"\nTesting manager {manager_id}")
print("Manager name:", get_manager_name(manager_id))

# Check manager tactical components
manager_tactical_components = manager_tactics.get(manager_id, [])
print("Manager tactical components:", manager_tactical_components)

# Get the best tactical component for this manager
best_manager_component = None
best_count = 0

for component_info in manager_tactical_components:
    if isinstance(component_info, dict) and 'count' in component_info:
        if component_info['count'] > best_count:
            best_count = component_info['count']
            best_manager_component = component_info.get('tactic')

print("Best manager component:", best_manager_component)
print("Best count:", best_count)

# Test get_top_players_for_manager function
print("\nTesting get_top_players_for_manager...")
try:
    top_players = get_top_players_for_manager(manager_id)
    print("Number of top players found:", len(top_players))
    if top_players:
        print("First player:", top_players[0])
    else:
        print("No players found")
except Exception as e:
    print("Error in get_top_players_for_manager:", str(e))
    import traceback
    traceback.print_exc()