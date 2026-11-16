# Usage Guide

## Starting the Application

1. Make sure you have Python installed (version 3.8 or higher recommended)
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your web browser and navigate to `http://127.0.0.1:5000`

## Using the Dashboard

### Player Selection
- Use the dropdown menu at the top to select a player
- The tactical impact simulation chart will automatically update

### Viewing Recommendations
- The "All Player Recommendations" table shows impact scores for different tactical components
- Each player has 7 tactical components (Tactic_Component_1 through Tactic_Component_7)

### Interpreting Results
- Higher impact scores indicate more effective tactical components for a player
- The bar chart visualizes the predicted impact of different tactical approaches
- The simulation shows how a player's performance might change with different tactical adjustments

## Troubleshooting

### Model Loading Issues
If you see "Model not available" messages:
- This is expected if the pickle file cannot be loaded due to version incompatibilities
- The application will still display player data and recommendations table
- Only the interactive simulation feature requires the model

### Common Issues
1. **Port already in use**: If port 5000 is occupied, the app will automatically use another port
2. **File not found errors**: Ensure all data files (player.xlsx, player_model.csv) are in the project directory
3. **Permission errors**: On some systems, you may need to run the command prompt as administrator

## Customization

### Adding New Players
1. Add new player information to `player.xlsx`
2. Ensure the Player_ID follows the format "PXX" (e.g., P01, P02)
3. Restart the application to see new players in the dropdown

### Modifying Tactical Components
1. Update `player_model.csv` with new tactical components
2. The application expects 7 tactical components per player

## Development

### Project Structure
```
Analysis/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── USAGE.md            # This file
├── player.xlsx         # Player information
├── player_model.csv    # Model data
├── best_random_forest.pkl # Trained model
├── CP_model.ipynb      # Analysis notebook
├── templates/
│   └── index.html      # Dashboard template
└── screenshots/
    └── dashboard_info.txt # Screenshot documentation
```

### Modifying the Dashboard
- Edit `templates/index.html` to change the UI
- Modify `app.py` to change data processing or add new features
- Styles are included directly in the HTML template

## API Endpoints

- `/` - Main dashboard page
- `/recommendations` - Returns JSON data for the recommendations table
- `/player/<int:player_id>` - Returns JSON data for the tactical simulation chart

## Data Format

### Player Data (player.xlsx)
- Player_ID: Unique identifier (P01, P02, etc.)
- Common_Name: Player's full name
- Position: Playing position
- Team information and physical attributes

### Model Data (player_model.csv)
- Player_ID: Links to player information
- Tactic_Component_1 through Tactic_Component_7: Tactical component impact scores
- Various performance and tactical metrics

## License

This project is for educational purposes only. See README.md for more information.