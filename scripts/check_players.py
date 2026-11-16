import pandas as pd

# Load player data
player_data = pd.read_excel('player.xlsx')

# Get unique player IDs
player_ids = sorted(player_data['Player_ID'].unique())
print("Player IDs in system:")
for pid in player_ids:
    print(f"  {pid}")

print(f"\nTotal players: {len(player_ids)}")

# Check which images exist
import os
print("\nImage files available:")
image_files = os.listdir('static/images')
image_files.sort()
for img in image_files:
    print(f"  {img}")

# Check which players have images
print("\nPlayers with images:")
players_with_images = []
for pid in player_ids:
    image_path = f"static/images/{pid}_img.jpg"
    if os.path.exists(image_path):
        players_with_images.append(pid)
        print(f"  {pid} - Image exists")
    else:
        print(f"  {pid} - Image missing")

print(f"\nPlayers with images: {len(players_with_images)}/{len(player_ids)}")