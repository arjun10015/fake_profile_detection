from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import joblib
import os
import numpy as np

app = Flask(__name__, static_folder='static')
CORS(app)

# Load your trained ML model (replace with actual model)
# model = joblib.load('model.pkl')

# Dummy prediction function (replace with actual model prediction)
def predict_fake_profiles(df):
    # Example: Random predictions for demonstration
    np.random.seed(42)
    return {
        "fake_profiles": df.iloc[np.random.choice(df.index, size=2, replace=False)].to_dict('records'),
        "stats": {
            "total": len(df),
            "fake_count": 2,
            "risk_level": "High"
        }
    }

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        df = pd.read_csv(file)
        # Add actual prediction logic here
        # predictions = model.predict(df)
        # results = df[predictions == 1].to_dict('records')
        
        results = predict_fake_profiles(df)
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)