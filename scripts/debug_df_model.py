import pandas as pd

# Load df_model
df_model = pd.read_csv('df_model.csv')

print("df_model loaded successfully")
print("Shape:", df_model.shape)
print("Columns:", df_model.columns.tolist())

# Check if Tactic_Component_1 exists
print("Tactic_Component_1 in columns:", 'Tactic_Component_1' in df_model.columns)

# Check sample data
print("Sample rows:")
print(df_model.head())

# Check unique Player_IDs
print("Unique Player_IDs:", len(df_model['Player_ID'].unique()))

# Check if a specific player exists
sample_player = df_model['Player_ID'].iloc[0] if len(df_model) > 0 else None
print("Sample player:", sample_player)

if sample_player:
    player_data = df_model[df_model['Player_ID'] == sample_player]
    print("Sample player data shape:", player_data.shape)
    print("Sample player Tactic_Component_1 mean:", player_data['Tactic_Component_1'].mean() if 'Tactic_Component_1' in player_data.columns else 'N/A')