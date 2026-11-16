import pandas as pd

# Load the data
df = pd.read_csv('player_model.csv')
features_to_drop = ['Player_ID', 'Manager_ID', 'Impact_Score']
feature_columns = [col for col in df.columns if col not in features_to_drop]

print("Feature columns:", len(feature_columns))
print("First 10 feature columns:", feature_columns[:10])

# Calculate mean for all feature columns
component_contributions = df[feature_columns].mean()
print("Type of component_contributions:", type(component_contributions))
print("Has index:", hasattr(component_contributions, 'index'))
print("Has values:", hasattr(component_contributions, 'values'))

# Try to access index and values
if hasattr(component_contributions, 'index'):
    print("Index type:", type(component_contributions.index))
    print("First 5 index items:", list(component_contributions.index)[:5])

if hasattr(component_contributions, 'values'):
    print("Values type:", type(component_contributions.values))
    print("First 5 values:", list(component_contributions.values)[:5])

# Test creating lists
variable_names = list(component_contributions.index)
contribution_values = list(component_contributions.values)
print("Variable names length:", len(variable_names))
print("Contribution values length:", len(contribution_values))