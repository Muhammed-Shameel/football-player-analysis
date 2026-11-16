import pandas as pd

# Load the same data as in app.py
manager_data = pd.read_excel('manager.xlsx')

# Simulate the logic from app.py
def get_manager_name(manager_id):
    manager_matches = manager_data[manager_data['Manager_ID'] == manager_id]
    if len(manager_matches) > 0:
        manager_list = []
        for idx in range(len(manager_matches)):
            row = manager_matches.iloc[idx]
            manager_list.append(row)
        
        manager_row = manager_list[0]
        print(f"Manager row type: {type(manager_row)}")
        print(f"Manager row: {manager_row}")
        
        # Handle both dictionary and pandas Series cases
        if isinstance(manager_row, dict) and 'Manager_Name' in manager_row:
            manager_name = str(manager_row['Manager_Name'])
            print("Using dict access")
        elif hasattr(manager_row, 'Manager_Name'):
            # Handle pandas Series case
            manager_name = str(manager_row.Manager_Name)
            print("Using attribute access")
        elif 'Manager_Name' in manager_row:
            # Handle pandas Series dictionary-like access
            manager_name = str(manager_row['Manager_Name'])
            print("Using key access")
        else:
            manager_name = str(manager_id)
            print("Using fallback")
        
        return manager_name
    return manager_id

# Test with M03
result = get_manager_name("M03")
print(f"Result: {result}")