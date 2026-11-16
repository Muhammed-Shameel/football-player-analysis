import pandas as pd

# Check team data structure
team_data = pd.read_excel('team.xlsx')
print("Team data columns:", team_data.columns.tolist())
print("Team data shape:", team_data.shape)
print("First few rows:")
print(team_data.head())

# Check player data structure
player_data = pd.read_excel('player.xlsx')
print("\nPlayer data columns:", player_data.columns.tolist())
print("Player data shape:", player_data.shape)
print("First few rows:")
print(player_data.head())

# Check manager data structure
manager_data = pd.read_excel('manager.xlsx')
print("\nManager data columns:", manager_data.columns.tolist())
print("Manager data shape:", manager_data.shape)
print("First few rows:")
print(manager_data.head())