import pandas as pd

# Test the manager formations data
try:
    df = pd.read_excel('manager_formation.xlsx')
    print("Manager formations data shape:", df.shape)
    print("Manager formations columns:", df.columns.tolist())
    print("Sample data:")
    print(df.head())
    
    # Check if we can group by Manager_ID
    formations_dict = {}
    for _, row in df.iterrows():
        manager_id = str(row['Manager_ID'])
        formation = str(row['Formation'])
        if manager_id not in formations_dict:
            formations_dict[manager_id] = []
        formations_dict[manager_id].append(formation)
    
    print("\nFormations dict sample (first 5):")
    for i, (manager_id, formations) in enumerate(formations_dict.items()):
        if i >= 5:
            break
        print(f"{manager_id}: {formations}")
        
except Exception as e:
    print("Error:", str(e))