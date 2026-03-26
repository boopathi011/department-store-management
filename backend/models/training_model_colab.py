import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 1. GENERATE SYNTHETIC DATA
# visits, total_spend, orders_count, product_views, discount_usage
def generate_data(n=1000):
    np.random.seed(42)
    visits = np.random.randint(1, 100, n)
    spend = np.random.randint(50, 5000, n)
    orders = np.random.randint(0, 50, n)
    views = np.random.randint(5, 500, n)
    discounts = np.random.randint(0, 2, n)
    
    # Label: 1 if Top Customer, 0 otherwise
    # Logic: High spend and high orders
    labels = ((spend > 2500) & (orders > 20)).astype(int)
    
    return pd.DataFrame({
        'visits': visits,
        'spend': spend,
        'orders': orders,
        'views': views,
        'discount': discounts,
        'label': labels
    })

data = generate_data()
X = data.drop('label', axis=1)
y = data['label']

# 2. TRAIN MODEL
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 3. SAVE AS PKL
with open('store_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as store_model.pkl")
print(f"Accuracy: {model.score(X_test, y_test)}")
