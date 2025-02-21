import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from preprocess import load_dataset  # Import feature extraction function

# Load dataset with extracted features
dataset_path = "../datasets/phishing_data.csv"
data = load_dataset(dataset_path)

# Separate features and labels
X = data.drop(columns=["label"])  # Features
y = data["label"]  # Target labels

print("Features used for training:", X.columns.tolist())

# Split dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Gradient Boosting Model (Better than Random Forest for small datasets)
model = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# Save the trained model
joblib.dump(model, "../ml_model/phishing_detector.pkl")
print("✅ Model saved successfully as phishing_detector.pkl")
