import pandas as pd
import json

# Load the same data as in app.py
manager_data = pd.read_excel('manager.xlsx')
manager_formation_data = pd.read_excel('manager_formation.xlsx')

# Load manager tactics mapping
import json
with open('manager_tactics.json', 'r') as f:
    manager_tactics = json.load(f)

# Simulate the get_manager_formations function
def get_manager_formations():
    """Get manager formations from the manager_formation.xlsx file"""
    try:
        formations = {}
        for _, row in manager_formation_data.iterrows():
            manager_id = str(row['Manager_ID'])
            formation = str(row['Formation'])
            if manager_id not in formations:
                formations[manager_id] = []
            formations[manager_id].append(formation)
        return formations
    except Exception as e:
        print(f"Error loading manager formations: {e}")
        return {}

# Simulate the logic for getting recommended managers
def simulate_get_managers():
    # Use the same data as would be used in the actual function
    manager_id = "M03"
    manager_formations = get_manager_formations()
    
    # Get manager info
    manager_matches = manager_data[manager_data['Manager_ID'] == manager_id]
    if len(manager_matches) > 0:
        # Convert to list to avoid pandas-specific methods
        manager_list = []
        for idx in range(len(manager_matches)):
            row = manager_matches.iloc[idx]
            manager_list.append(row)
        
        manager_row = manager_list[0]
        # Handle both dictionary and pandas Series cases
        if isinstance(manager_row, dict) and 'Manager_Name' in manager_row:
            manager_name = str(manager_row['Manager_Name'])
        elif hasattr(manager_row, 'Manager_Name'):
            # Handle pandas Series case
            manager_name = str(manager_row.Manager_Name)
        elif 'Manager_Name' in manager_row:
            # Handle pandas Series dictionary-like access
            manager_name = str(manager_row['Manager_Name'])
        else:
            manager_name = str(manager_id)
        
        print(f"Manager ID: {manager_id}")
        print(f"Manager Name: {manager_name}")
        print(f"Type of manager_row: {type(manager_row)}")
        
        # Get formations for this manager
        formations = manager_formations.get(manager_id, [])
        print(f"Formations: {formations}")
        
        return {
            'Manager_ID': str(manager_id),
            'Manager_Name': manager_name,
            'formations': formations
        }
    
    return None

# Run the test
result = simulate_get_managers()
print(f"Result: {json.dumps(result, indent=2)}")