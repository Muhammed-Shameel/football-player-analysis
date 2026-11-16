import pandas as pd

# Load manager data
manager_data = pd.read_excel('manager.xlsx')

# Test accessing manager name for M03
manager_id = "M03"
manager_matches = manager_data[manager_data['Manager_ID'] == manager_id]

if len(manager_matches) > 0:
    manager_row = manager_matches.iloc[0]
    print("Manager ID:", manager_id)
    print("Manager Name (attribute):", manager_row.Manager_Name)
    print("Manager Name (key access):", manager_row['Manager_Name'])
    print("Type of manager_row:", type(manager_row))