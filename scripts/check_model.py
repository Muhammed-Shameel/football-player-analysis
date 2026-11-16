import pickle
import numpy as np

# Load the XGBoost model
model = pickle.load(open('xgboost_best.pkl', 'rb'))
print(f'Model feature count: {model.n_features_in_}')

# Try to get feature names if available
if hasattr(model.get_booster(), 'feature_names'):
    print(f'Model booster feature names: {model.get_booster().feature_names}')
else:
    print('Feature names not available')