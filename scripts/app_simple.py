import pandas as pd
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify
import os
import warnings
import json
from collections import defaultdict

# Suppress warnings
warnings.filterwarnings("ignore")

app = Flask(__name__, template_folder='templates', static_folder='static')

# Global variables for data
player_data = None
tactic_data = None
team_data = None
manager_data = None
manager_formation_data = None
manager_tactics = {}
players_df = pd.DataFrame()
years = []

def load_data():
    """Load all required data files with error handling"""
    global player_data, tactic_data, team_data, manager_data
    global manager_formation_data, manager_tactics, players_df, years
    
    try:
        if os.path.exists('player.xlsx'):
            player_data = pd.read_excel('player.xlsx')
            print("✓ Loaded player.xlsx")
        else:
            print("⚠ player.xlsx not found")
            player_data = pd.DataFrame()
            
        if os.path.exists('df_model.csv'):
            tactic_data = pd.read_csv('df_model.csv')
            print("✓ Loaded df_model.csv")
        else:
            print("⚠ df_model.csv not found")
            tactic_data = pd.DataFrame()
            
        if os.path.exists('team.xlsx'):
            team_data = pd.read_excel('team.xlsx')
            print("✓ Loaded team.xlsx")
        else:
            print("⚠ team.xlsx not found")
            team_data = pd.DataFrame()
            
        if os.path.exists('manager.xlsx'):
            manager_data = pd.read_excel('manager.xlsx')
            print("✓ Loaded manager.xlsx")
        else:
            print("⚠ manager.xlsx not found")
            manager_data = pd.DataFrame()
            
        if os.path.exists('manager_formation.xlsx'):
            manager_formation_data = pd.read_excel('manager_formation.xlsx')
            print("✓ Loaded manager_formation.xlsx")
        else:
            print("⚠ manager_formation.xlsx not found")
            manager_formation_data = pd.DataFrame()
            
        if os.path.exists('manager_tactics.json'):
            with open('manager_tactics.json', 'r') as f:
                manager_tactics = json.load(f)
            print("✓ Loaded manager_tactics.json")
        else:
            print("⚠ manager_tactics.json not found")
            manager_tactics = {}
            
        # Process player data for dropdown
        if not player_data.empty and 'Player_ID' in player_data.columns and 'Common_Name' in player_data.columns:
            players_df = player_data[['Player_ID', 'Common_Name']].drop_duplicates()
            players_df.columns = ['Player_ID', 'Player_Name']  # Rename for consistency
            print(f"✓ Processed {len(players_df)} unique players")
        else:
            players_df = pd.DataFrame(columns=['Player_ID', 'Player_Name'])
            print("⚠ No player data available")
            
        # Get years from tactic data
        if not tactic_data.empty and 'Year' in tactic_data.columns:
            years = sorted(tactic_data['Year'].unique())
            print(f"✓ Found data for years: {years}")
        else:
            years = []
            print("⚠ No year data available")
            
    except Exception as e:
        print(f"Error loading data: {e}")

# Load data when the app starts
load_data()

# Available models
MODELS = {
    'Random Forest': 'randomforest_best.pkl',
    'Gradient Boosting': 'gradientboost_best.pkl',
    'XGBoost': 'xgboost_best.pkl',
    'Neural Network': 'neuralnet_best.pkl'
}

@app.route('/')
def index():
    """Main dashboard page"""
    # Convert DataFrame to list of dictionaries
    player_list = []
    for _, row in players_df.iterrows():
        player_list.append({
            'Player_ID': row['Player_ID'],
            'Player_Name': row['Player_Name']
        })
    
    return render_template('index.html', 
                         players=player_list,
                         models=list(MODELS.keys()),
                         years=years)

@app.route('/managers')
def managers_page():
    """Managers recommendation page"""
    # Convert DataFrame to list of dictionaries
    player_list = []
    for _, row in players_df.iterrows():
        player_list.append({
            'Player_ID': row['Player_ID'],
            'Player_Name': row['Player_Name']
        })
    
    # Get the player_id from URL parameters if available
    player_id = request.args.get('player_id')
    
    return render_template('managers.html', 
                         players=player_list,
                         models=list(MODELS.keys()),
                         years=years,
                         selected_player_id=player_id)

@app.route('/insights')
def insights_page():
    """Insights page"""
    # Convert DataFrame to list of dictionaries
    player_list = []
    for _, row in players_df.iterrows():
        player_list.append({
            'Player_ID': row['Player_ID'],
            'Player_Name': row['Player_Name']
        })
    
    return render_template('insights.html', 
                         players=player_list,
                         models=list(MODELS.keys()),
                         years=years)

@app.route('/get_player_info')
def get_player_info():
    """API endpoint to get player information"""
    player_id = request.args.get('player_id')
    
    # Initialize response
    response_data = {
        'Player_ID': player_id,
        'Common_Name': None,
        'Team_ID': None,
        'Team_Name': None,
        'Position': None,
        'Impact_Score': None,
        'BMI': None,
        'image_exists': False,
        'image_path': None
    }
    
    if not player_id:
        response_data['error'] = 'Player ID is required'
        return jsonify(response_data), 400
    
    if player_data is None or player_data.empty:
        response_data['error'] = 'Player data not available'
        return jsonify(response_data), 404
    
    # Get player info
    player_matches = player_data[player_data['Player_ID'] == player_id]
    if len(player_matches) == 0:
        response_data['error'] = 'Player not found'
        return jsonify(response_data), 404
    
    try:
        player_info = player_matches.iloc[0]
        
        # Update response with player info
        response_data['Common_Name'] = player_info.get('Common_Name', 'Unknown Player')
        response_data['Team_ID'] = player_info.get('Team_ID', None)
        response_data['Position'] = player_info.get('Position', 'Unknown Position')
        response_data['BMI'] = player_info.get('BMI', None)
        
        # Check if image exists
        image_path = os.path.join("static", "images", f"{player_id}_img.jpg")
        image_exists = os.path.exists(image_path)
        response_data['image_exists'] = image_exists
        response_data['image_path'] = f"/{image_path.replace(os.sep, '/')}" if image_exists else None
        
        # Get team name if team_id exists
        if response_data['Team_ID'] and team_data is not None and not team_data.empty:
            team_matches = team_data[team_data['Team_ID'] == response_data['Team_ID']]
            if len(team_matches) > 0:
                response_data['Team_Name'] = team_matches.iloc[0].get('Team_Name', response_data['Team_ID'])
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error processing player info: {e}")
        response_data['error'] = 'Error processing player information'
        return jsonify(response_data), 500

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint to get tactical recommendations"""
    player_id = request.form.get('player_id')
    
    if not player_id:
        return jsonify({'error': 'Player ID is required'}), 400
    
    # Return mock data for now
    recommendations = [
        {'component': 'Tactic_Component_1', 'value': 0.85, 'impact': 0.85},
        {'component': 'Tactic_Component_2', 'value': 0.72, 'impact': 0.72},
        {'component': 'Tactic_Component_3', 'value': 0.68, 'impact': 0.68},
        {'component': 'Tactic_Component_4', 'value': 0.91, 'impact': 0.91},
        {'component': 'Tactic_Component_5', 'value': 0.55, 'impact': 0.55},
        {'component': 'Tactic_Component_6', 'value': 0.78, 'impact': 0.78},
        {'component': 'Tactic_Component_7', 'value': 0.82, 'impact': 0.82}
    ]
    
    # Find best component
    best_component = max(recommendations, key=lambda x: x['value'])
    
    # Mock scores
    scores = {
        'Passing': 85.5,
        'Shooting': 78.2,
        'Creativity': 82.1,
        'Dribbling': 76.8,
        'Defense': 72.4,
        'Impact_Score': 80.3
    }
    
    # Mock managers
    recommended_managers = [
        {
            'Manager_ID': 'M01',
            'Manager_Name': 'John Smith',
            'tactic_count': 45,
            'relevance_score': 0.85,
            'formations': ['4-4-2', '4-3-3']
        },
        {
            'Manager_ID': 'M02',
            'Manager_Name': 'Mike Johnson',
            'tactic_count': 38,
            'relevance_score': 0.72,
            'formations': ['3-5-2', '4-2-3-1']
        }
    ]
    
    response_data = {
        'recommended_managers': recommended_managers,
        'recommendations': recommendations,
        'best_component': best_component,
        'scores': scores
    }
    
    return jsonify(response_data)

@app.route('/get_managers_for_player', methods=['POST'])
def get_managers_for_player():
    """API endpoint to get recommended managers for a player"""
    player_id = request.form.get('player_id')
    
    if not player_id:
        return jsonify({'error': 'Player ID is required'}), 400
    
    # Return mock data for now
    recommended_managers = [
        {
            'Manager_ID': 'M01',
            'Manager_Name': 'John Smith',
            'tactic_count': 45,
            'relevance_score': 0.85,
            'formations': ['4-4-2', '4-3-3']
        },
        {
            'Manager_ID': 'M02',
            'Manager_Name': 'Mike Johnson',
            'tactic_count': 38,
            'relevance_score': 0.72,
            'formations': ['3-5-2', '4-2-3-1']
        },
        {
            'Manager_ID': 'M03',
            'Manager_Name': 'Sarah Williams',
            'tactic_count': 32,
            'relevance_score': 0.65,
            'formations': ['4-4-2', '5-3-2']
        }
    ]
    
    return jsonify({'recommended_managers': recommended_managers})

@app.route('/get_manager_summary')
def get_manager_summary_endpoint():
    """API endpoint to get manager-level tactic usage summary"""
    # Return mock data for now
    summary = {
        "M01": {
            "tactics": [{"tactic": "Tactic_Component_1", "count": 91}],
            "main_tactic": {"tactic": "Tactic_Component_1", "count": 91}
        },
        "M02": {
            "tactics": [
                {"tactic": "Tactic_Component_2", "count": 31},
                {"tactic": "Tactic_Component_6", "count": 288}
            ],
            "main_tactic": {"tactic": "Tactic_Component_6", "count": 288}
        }
    }
    return jsonify(summary)

if __name__ == '__main__':
    print("Starting Football Tactical Recommendations Dashboard...")
    print("Make sure you have the required data files in the project directory.")
    print("Access the dashboard at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)