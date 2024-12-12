import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model 
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Initialize Flask app
app = Flask(__name__, static_folder='build/static', template_folder='build')
CORS(app)  # Enable CORS for React frontend

@app.route('/')
def serve():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.static_folder), path)

# Load the model
model = load_model(r'.\face_model.h5')

# Define the emotion labels
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# Function to preprocess image
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (48, 48))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)
    return img

# Function to predict emotion
def predict_emotion(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    emotion_index = np.argmax(prediction)
    emotion = emotion_labels[emotion_index]  # Get the corresponding emotion label
    confidence = np.max(prediction) * 100  # Calculate confidence
    return emotion, float(confidence)  # Convert confidence to float

# API endpoint for emotion detection and song recommendation
@app.route('/detect-emotion', methods=['GET', 'POST'])
def detect_emotion():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file temporarily
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)  # Create folder if it doesn't exist
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    try:
        # Predict emotion
        emotion, confidence = predict_emotion(file_path)
        
        # Print the confidence value for debugging
        print(f"Predicted Emotion: {emotion}, Confidence: {confidence}%")
        
        # Get song recommendations based on emotion
        recommendations = recommend_songs(emotion, data)
        
        # Format recommendations to return in response
        recommendations_list = recommendations.to_dict(orient='records')
        
        return jsonify({
            "emotion": emotion, 
            "confidence": int(confidence), 
            "recommendations": recommendations_list
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)  # Clean up the file after processing

# Load datasets
data = pd.read_csv(r"C:\Users\dsilv\development\Emotion\backend\data\data.csv")

# Emotion-to-features mapping
emotion_to_features = {
    "Angry": {"valence": 0.2, "energy": 0.9, "tempo": 120},
    "Disgust": {"valence": 0.3, "energy": 0.5, "tempo": 80},
    "Fear": {"valence": 0.2, "energy": 0.8, "tempo": 140},
    "Happy": {"valence": 0.9, "energy": 0.8, "tempo": 140},
    "Sad": {"valence": 0.2, "energy": 0.3, "tempo": 60},
    "Surprise": {"valence": 0.8, "energy": 0.7, "tempo": 160},
    "Neutral": {"valence": 0.5, "energy": 0.5, "tempo": 100},
}

def recommend_songs(emotion, data, num_songs=4):
    # Get target features for the emotion
    target_features = emotion_to_features.get(emotion)
    if not target_features:
        return f"Emotion '{emotion}' is not recognized."
    
    # Normalize the features in the dataset
    scaler = MinMaxScaler()
    normalized_data = data[['valence', 'energy', 'tempo']].copy()
    normalized_data[['valence', 'energy', 'tempo']] = scaler.fit_transform(normalized_data)
    
    # Normalize the target emotion features
    target_vector = scaler.transform(
        np.array([[target_features['valence'], target_features['energy'], target_features['tempo']]]))
    
    # Calculate cosine similarity
    similarities = cosine_similarity(normalized_data, target_vector).flatten()
    data['similarity'] = similarities
    
    # Shuffle and select top matches
    top_matches = data.sort_values(by='similarity', ascending=False).head(20)
    recommended = top_matches.sample(n=min(num_songs, len(top_matches)), random_state=None)
    
    # Format the output
    formatted_recommendations = recommended[['name', 'artists', 'valence', 'energy', 'tempo']].reset_index(drop=True)
    return formatted_recommendations

# Main function to run the app
if __name__ == "__main__":
    app.run(debug=True)
