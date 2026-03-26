import pickle
import numpy as np

import os

# Correct path relative to this file
MODEL_PATH = os.path.join(os.path.dirname(__file__), "store_model.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except:
    model = None

def predict_customer(visits, spend, orders, views, discount):
    if not model: return "Model Unavailable"
    data = np.array([[visits, spend, orders, views, discount]])
    pred = model.predict(data)[0]
    return "Top Customer" if pred == 1 else "Normal Customer"

if __name__ == "__main__":
    # example
    print(predict_customer(10, 500, 8, 20, 1))
