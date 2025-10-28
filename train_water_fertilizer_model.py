import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# ===========================
# Paths
# ===========================
DATA_PATH = "datasets/Crop_recommendation.csv"  # <-- must include 'Soil' column now
MODEL_PATH = "models/crop_recommendation_model.pkl"

os.makedirs("models", exist_ok=True)

# ===========================
# Load dataset
# ===========================
data = pd.read_csv(DATA_PATH)

# Expected columns:
# N, P, K, temperature, humidity, ph, rainfall, Soil, label

# ===========================
# Encode Soil and Label
# ===========================
soil_encoder = LabelEncoder()
data["Soil_encoded"] = soil_encoder.fit_transform(data["Soil"])

label_encoder = LabelEncoder()
data["label_encoded"] = label_encoder.fit_transform(data["label"])

# ===========================
# Feature selection
# ===========================
X = data[["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "Soil_encoded"]]
y = data["label_encoded"]

# ===========================
# Scale numerical features
# ===========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===========================
# Train/test split
# ===========================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# ===========================
# Train XGBoost model
# ===========================
model = XGBClassifier(
    n_estimators=250,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.2,
    eval_metric="mlogloss",
    random_state=42,
    use_label_encoder=False
)

model.fit(X_train, y_train)

# ===========================
# Evaluate
# ===========================
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f" Model trained successfully with Soil feature. Accuracy: {acc*100:.2f}%")

# ===========================
# Save model + encoders
# ===========================
joblib.dump({
    "model": model,
    "scaler": scaler,
    "label_encoder": label_encoder,
    "soil_encoder": soil_encoder
}, MODEL_PATH)

print(f" Model and encoders saved at: {MODEL_PATH}")
