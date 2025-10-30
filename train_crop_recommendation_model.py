import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

os.makedirs("models", exist_ok=True)

# ======================
# Load Dataset
# ======================
data = pd.read_csv("datasets/Crop_recommendation.csv")

#  Ensure Soil column exists
if "soil" not in data.columns:
    raise ValueError(" 'Soil' column not found in dataset! Please add it before training.")

# ======================
# Encode Soil Type
# ======================
soil_encoder = LabelEncoder()
data["Soil_encoded"] = soil_encoder.fit_transform(data["soil"])

# ======================
# Feature and Label Split
# ======================
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'Soil_encoded']]
y = data['label']

# Encode target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Scale numerical features (but not Soil)
scaler = StandardScaler()
X_scaled = X.copy()
X_scaled[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall','Soil_encoded']] = scaler.fit_transform(
    X[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall','Soil_encoded']]
)

# ======================
# Split Data
# ======================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# ======================
# Train XGBoost
# ======================
model = XGBClassifier(
    n_estimators=150,
    learning_rate=0.04,
    max_depth=6,
    subsample=0.7,
    colsample_bytree=0.4,
    gamma=0.03,
    random_state=42,
    eval_metric="mlogloss"
)
model.fit(X_train, y_train)

# ======================
# Evaluate Model
# ======================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f" Model Accuracy: {accuracy * 100:.2f}%")

# ======================
# Save Model + Encoders
# ======================
joblib.dump({
    'model': model,
    'scaler': scaler,
    'label_encoder': label_encoder,
    'soil_encoder': soil_encoder
}, 'models/crop_recommendation_model.pkl')

print(" Model saved successfully at models/crop_recommendation_model.pkl")