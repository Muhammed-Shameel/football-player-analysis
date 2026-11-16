import os

# Available machine learning models and their file mappings
MODELS = {
    'Random Forest': os.path.join('models', 'randomforest_best.pkl'),
    'Gradient Boosting': os.path.join('models', 'gradientboost_best.pkl'),
    'XGBoost': os.path.join('models', 'xgboost_best.pkl'),
    'Neural Network': os.path.join('models', 'neuralnet_best.pkl'),
    'SVM': os.path.join('models', 'svm_best_model.pkl')
}

# Global model performance scores (F1 scores)
MODEL_PERFORMANCE = {
    'Random Forest': 0.64,
    'Gradient Boosting': 0.65,
    'XGBoost': 0.66,
    'Neural Network': 0.62,
    'SVM': 0.65
}

# Determine best model globally
BEST_MODEL = max(MODEL_PERFORMANCE.keys(), key=lambda k: MODEL_PERFORMANCE[k])

# Data file paths
PLAYER_DATA_PATH = os.path.join('data', 'player.xlsx')
DF_MODEL_PATH = os.path.join('data', 'df_model.csv')
TEAM_DATA_PATH = os.path.join('data', 'team.csv')
MANAGER_DATA_PATH = os.path.join('data', 'manager.xlsx')
MANAGER_FORMATION_PATH = os.path.join('data', 'manager_formation.xlsx')
MANAGER_TACTICS_PATH = os.path.join('data', 'manager_tactics.json')
MANAGER_TACTIC_SUMMARY_PATH = os.path.join('data', 'manager_tactic_summary.json')
LABEL_ENCODER_PATH = os.path.join('models', 'label_encoder.pkl')
