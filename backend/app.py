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
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

app = Flask(__name__, static_folder='build/static', template_folder='build')
CORS(app)

@app.route('/')
def serve():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.static_folder), path)

model = load_model(r'.\models\new.h5')

data = pd.read_csv(r"C:\Users\dsilv\development\Emotion\backend\data\data.csv")

client_id = "1f35b2325d49492394d29449ecad5656"
client_secret = "bf068d1d64b3493587d891f8320dfb2e"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

emotion_to_features = {
    "Angry": {"valence": 0.2, "energy": 0.9, "tempo": 120},
    "Disgust": {"valence": 0.3, "energy": 0.5, "tempo": 80},
    "Fear": {"valence": 0.2, "energy": 0.8, "tempo": 140},
    "Happy": {"valence": 0.9, "energy": 0.8, "tempo": 140},
    "Sad": {"valence": 0.2, "energy": 0.3, "tempo": 60},
    "Surprise": {"valence": 0.8, "energy": 0.7, "tempo": 160},
    "Neutral": {"valence": 0.5, "energy": 0.5, "tempo": 100},
}

emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (48, 48))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)
    return img

def predict_emotion(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    emotion_index = np.argmax(prediction)
    emotion = emotion_labels[emotion_index]
    confidence = (np.max(prediction) * 100) 
    return emotion, float(confidence)

def get_album_art(song_name, artist_name):
    query = f"{song_name} {artist_name}"
    result = sp.search(query, limit=1, type='track')
    if result['tracks']['items']:
        album_url = result['tracks']['items'][0]['album']['images'][0]['url']
        return album_url
    return None
def get_spotify_url(song_name, artist_name):
    query = f"{song_name} {artist_name}"
    result = sp.search(query, limit=1, type='track')
    if result['tracks']['items']:
        song_url = result['tracks']['items'][0]['external_urls']['spotify']
        return song_url
    return None

def get_spotify_embed_url(song_name, artist_name):
    query = f"{song_name} {artist_name}"
    result = sp.search(query, limit=1, type='track')
    if result['tracks']['items']:
        track_id = result['tracks']['items'][0]['id']
        embed_url = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0"
        return embed_url
    return None


# Update the recommend_songs function
def recommend_songs(emotion, data, num_songs=6):
    target_features = emotion_to_features.get(emotion)
    if not target_features:
        return f"Emotion '{emotion}' is not recognized."

    scaler = MinMaxScaler()
    normalized_data = data[['valence', 'energy', 'tempo']].copy()
    normalized_data[['valence', 'energy', 'tempo']] = scaler.fit_transform(normalized_data)

    target_vector = scaler.transform(
        np.array([[target_features['valence'], target_features['energy'], target_features['tempo']]])
    )

    similarities = cosine_similarity(normalized_data, target_vector).flatten()
    data['similarity'] = similarities

    top_matches = data.sort_values(by='similarity', ascending=False).head(20)
    recommended = top_matches.sample(n=min(num_songs, len(top_matches)), random_state=None)

    recommended['image'] = recommended.apply(lambda row: get_album_art(row['name'], row['artists']), axis=1)
    recommended['url'] = recommended.apply(lambda row: get_spotify_url(row['name'], row['artists']), axis=1)
    recommended['embed_url'] = recommended.apply(lambda row: get_spotify_embed_url(row['name'], row['artists']), axis=1)

    formatted_recommendations = recommended[['name', 'artists', 'valence', 'energy', 'tempo', 'image', 'url', 'embed_url']].reset_index(drop=True)
    return formatted_recommendations

@app.route('/detect-emotion', methods=['POST'])
def detect_emotion():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        emotion, confidence = predict_emotion(file_path)

        recommended_songs = recommend_songs(emotion, data)

        os.remove(file_path)
        
        return jsonify({
            "emotion": emotion,
            "confidence": int(confidence),
            "recommended_songs": recommended_songs.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
