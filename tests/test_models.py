import pickle
import pandas as pd

# Test all available models
models = {
    'RandomForest_tactic_model.pkl',
    'XGBoost_tactic_model.pkl',
    'GradientBoost_tactic_model.pkl'
}

for model_name in models:
    try:
        with open(model_name, 'rb') as f:
            model = pickle.load(f)
        print(f"SUCCESS: {model_name} loaded successfully!")
        print(f"  Model type: {type(model)}")
        if hasattr(model, 'get_params'):
            print(f"  Model params: {model.get_params()}")
        print()
    except Exception as e:
        print(f"ERROR loading {model_name}: {e}")
        print(f"  Error type: {type(e)}")
        print()