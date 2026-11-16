import os

# Test image paths
player_ids = [f"P{i:02d}" for i in range(1, 16)]  # P01 to P15

print("Testing image paths:")
for pid in player_ids:
    # Current path used in the app
    current_path = f"static/images/{pid}_img.jpg"
    full_path = os.path.join("static", "images", f"{pid}_img.jpg")
    
    exists = os.path.exists(full_path)
    status = "✓" if exists else "✗"
    
    print(f"{status} {pid}: {current_path} ({'exists' if exists else 'missing'})")
    
    if not exists:
        # Check if file exists with different naming
        possible_files = [f for f in os.listdir("static/images") if f.startswith(pid)]
        if possible_files:
            print(f"  Found similar files: {possible_files}")