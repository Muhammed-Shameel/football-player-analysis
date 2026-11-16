import pickle
import pandas as pd

# Try to load the pickle file and see what's in it
try:
    with open('best_random_forest.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
    print(f"Model type: {type(model)}")
    print(f"Model: {model}")
except Exception as e:
    print(f"Error loading model: {e}")
    print(f"Error type: {type(e)}")