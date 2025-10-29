# train_water_fertilizer_model_training.py
import pandas as pd
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Paths
DATA_PATH = "datasets/crop_water_fertilizer_plan.csv"
MODEL_PATH = "models/water_fertilizer_model.pkl"
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

# Encode
crop_encoder = LabelEncoder()
df['Crop_encoded'] = crop_encoder.fit_transform(df['Crop'])

irrigation_encoder = LabelEncoder()
df['Irrigation_encoded'] = irrigation_encoder.fit_transform(df['Irrigation'])

notes_encoder = LabelEncoder()
df['Notes_encoded'] = notes_encoder.fit_transform(df['Notes'])

# Features + target
X = df[['Crop_encoded', 'N', 'P', 'K', 'pH']]
y = df['Irrigation_encoded']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Train model
from xgboost import XGBClassifier
model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
model.fit(X_train, y_train)

# Accuracy
acc = accuracy_score(y_test, model.predict(X_test))
print(f"Model trained successfully. Accuracy: {acc * 100:.2f}%")

# Save model and encoders
with open(MODEL_PATH, "wb") as f:
    pickle.dump({
        "model": model,
        "crop_encoder": crop_encoder,
        "irrigation_encoder": irrigation_encoder,
        "notes_encoder": notes_encoder
    }, f)

print(f" Model saved to: {MODEL_PATH}")
