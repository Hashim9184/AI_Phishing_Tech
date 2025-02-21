from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml_model.preprocess import extract_features
app = Flask(__name__)

# Load trained model
model = joblib.load("../ml_model/phishing_detector.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Extract features
    features = extract_features(url)
    features_df = pd.DataFrame([features])

    # Ensure columns match exactly with the trained model
    model_features = model.feature_names_in_
    features_df = features_df.reindex(columns=model_features, fill_value=0)  # Fill missing columns with 0

    # Make prediction
    prediction = model.predict(features_df)[0]
    result = "Phishing" if prediction == 1 else "Legitimate"

    return jsonify({"url": url, "prediction": result})

if __name__ == '__main__':
    app.run(debug=True)
