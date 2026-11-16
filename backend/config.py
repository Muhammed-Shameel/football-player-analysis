import os

# Available machine learning models (restricted to the best model)
MODELS = {
    'XGBoost': os.path.join('models', 'xgboost_best.pkl')
}

# Global model performance scores (F1 scores)
MODEL_PERFORMANCE = {
    'XGBoost': 0.66
}

# Determine best model globally
BEST_MODEL = 'XGBoost'

# Data file paths
PLAYER_DATA_PATH = os.path.join('data', 'player.xlsx')
DF_MODEL_PATH = os.path.join('data', 'df_model.csv')
TEAM_DATA_PATH = os.path.join('data', 'team.csv')
MANAGER_DATA_PATH = os.path.join('data', 'manager.xlsx')
MANAGER_FORMATION_PATH = os.path.join('data', 'manager_formation.xlsx')
MANAGER_TACTICS_PATH = os.path.join('data', 'manager_tactics.json')
MANAGER_TACTIC_SUMMARY_PATH = os.path.join('data', 'manager_tactic_summary.json')
LABEL_ENCODER_PATH = os.path.join('models', 'label_encoder.pkl')
