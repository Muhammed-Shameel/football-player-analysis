import json
import pandas as pd

# Load manager tactics
with open('manager_tactics.json', 'r') as f:
    manager_tactics = json.load(f)

print("Manager tactics loaded successfully")
print("Sample data for M01:", manager_tactics.get('M01'))

# Check the structure
manager_id = 'M01'
manager_tactical_components = manager_tactics.get(manager_id, [])
print("Manager tactical components for M01:", manager_tactical_components)

# Get the best tactical component for this manager
best_manager_component = None
best_count = 0

for component_info in manager_tactical_components:
    print("Component info:", component_info)
    print("Type of component_info:", type(component_info))
    if isinstance(component_info, dict) and 'count' in component_info:
        if component_info['count'] > best_count:
            best_count = component_info['count']
            best_manager_component = component_info.get('tactic')

print("Best manager component:", best_manager_component)
print("Best count:", best_count)