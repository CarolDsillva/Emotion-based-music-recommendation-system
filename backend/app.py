import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model 

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
model = load_model(r'.\cnn_emotion_detection.h5')

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

# API endpoint for emotion detection
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
        
        return jsonify({"emotion": emotion, "confidence": int(confidence)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)  # Clean up the file after processing

# Main function to run the app
if __name__ == "__main__":
    app.run(debug=True)
