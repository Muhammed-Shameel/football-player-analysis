# Test to verify the manager name fix
import pandas as pd

# Load manager data (same as in app.py)
manager_data = pd.read_excel('manager.xlsx')

# Test the logic for manager M03
manager_id = "M03"
manager_matches = manager_data[manager_data['Manager_ID'] == manager_id]

if len(manager_matches) > 0:
    # Convert to list to avoid pandas-specific methods (same as in app.py)
    manager_list = []
    for idx in range(len(manager_matches)):
        row = manager_matches.iloc[idx]
        manager_list.append(row)
    
    manager_row = manager_list[0]
    print(f"Manager row type: {type(manager_row)}")
    print(f"Manager row: {manager_row}")
    
    # Test the fixed logic
    # Handle both dictionary and pandas Series cases
    if isinstance(manager_row, dict) and 'Manager_Name' in manager_row:
        manager_name = str(manager_row['Manager_Name'])
        print(f"Using dict access: {manager_name}")
    elif hasattr(manager_row, 'Manager_Name'):
        # Handle pandas Series case
        manager_name = str(manager_row.Manager_Name)
        print(f"Using attribute access: {manager_name}")
    elif 'Manager_Name' in manager_row:
        # Handle pandas Series dictionary-like access
        manager_name = str(manager_row['Manager_Name'])
        print(f"Using key access: {manager_name}")
    else:
        manager_name = str(manager_id)
        print(f"Using fallback: {manager_name}")
    
    print(f"Final manager name: {manager_name}")
else:
    print("No manager found")