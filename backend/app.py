"""
emuziek - Flask backend
Detects the emotion in a face photo with a CNN (FER-2013, 48x48 grayscale)
and recommends songs whose audio features (valence, energy, tempo) match it.
"""
import os

import cv2
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from sklearn.preprocessing import MinMaxScaler

try:  # optional: load backend/.env if python-dotenv is installed
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
from tensorflow.keras.models import load_model  # noqa: E402

# ---------------------------------------------------------------- paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_cnn.h5")
DATA_PATH = os.path.join(BASE_DIR, "data", "data.csv")
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
FRONTEND_BUILD = os.path.join(BASE_DIR, "..", "frontend", "build")

# ---------------------------------------------------------------- config
EMOTION_LABELS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# Target audio features for each emotion (valence & energy are 0-1, tempo in BPM)
EMOTION_TO_FEATURES = {
    "Angry":    {"valence": 0.2, "energy": 0.9, "tempo": 120},
    "Disgust":  {"valence": 0.3, "energy": 0.5, "tempo": 80},
    "Fear":     {"valence": 0.2, "energy": 0.8, "tempo": 140},
    "Happy":    {"valence": 0.9, "energy": 0.8, "tempo": 140},
    "Sad":      {"valence": 0.2, "energy": 0.3, "tempo": 60},
    "Surprise": {"valence": 0.8, "energy": 0.7, "tempo": 160},
    "Neutral":  {"valence": 0.5, "energy": 0.5, "tempo": 100},
}
FEATURES = ["valence", "energy", "tempo"]
MIN_POPULARITY = int(os.environ.get("MIN_POPULARITY", "40"))  # skip very obscure tracks
MAX_UPLOAD_MB = 10

# ---------------------------------------------------------------- load once at startup
model = load_model(MODEL_PATH, compile=False)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

songs = pd.read_csv(DATA_PATH)
songs = songs[songs["popularity"] >= MIN_POPULARITY].dropna(subset=FEATURES)
# the dataset lists some tracks several times (re-releases, remasters): keep the most popular copy
songs = (songs.sort_values("popularity", ascending=False)
              .drop_duplicates(subset=["name", "artists"])
              .reset_index(drop=True))
scaler = MinMaxScaler().fit(songs[FEATURES])
song_matrix = scaler.transform(songs[FEATURES])

# Spotify is optional: without credentials the app still recommends songs (no album art / player)
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
sp = None
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
        requests_timeout=5, retries=1,
    )

# ---------------------------------------------------------------- app
app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
CORS(app)


def preprocess_image(image_bytes):
    """bytes -> (1, 48, 48, 1) float tensor. Crops to the largest face if one is found."""
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Could not read the image. Please upload a JPG or PNG photo.")

    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    face_found = len(faces) > 0
    if face_found:
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])  # largest face
        img = img[y:y + h, x:x + w]

    img = cv2.resize(img, (48, 48)).astype("float32") / 255.0
    return img.reshape(1, 48, 48, 1), face_found


def predict_emotion(image_bytes):
    tensor, face_found = preprocess_image(image_bytes)
    probs = model.predict(tensor, verbose=0)[0]
    idx = int(np.argmax(probs))
    all_probs = {label: round(float(p) * 100, 1) for label, p in zip(EMOTION_LABELS, probs)}
    return EMOTION_LABELS[idx], float(probs[idx]) * 100, face_found, all_probs


def clean_artists(value):
    """Dataset stores artists like "['Adele', 'X']" -> "Adele, X"."""
    return str(value).strip("[]").replace("'", "").replace('"', "")


def spotify_lookup(song_name, artists):
    """One Spotify search per song -> (album_art, song_url, embed_url). Never raises."""
    if sp is None:
        return None, None, None
    try:
        items = sp.search(f"{song_name} {artists}", limit=1, type="track")["tracks"]["items"]
        if items:
            t = items[0]
            image = t["album"]["images"][0]["url"] if t["album"]["images"] else None
            embed = f"https://open.spotify.com/embed/track/{t['id']}?utm_source=generator&theme=0"
            return image, t["external_urls"]["spotify"], embed
    except Exception as e:  # network error, bad credentials, rate limit...
        app.logger.warning("Spotify lookup failed for %s: %s", song_name, e)
    return None, None, None


def recommend_songs(emotion, num_songs=6, pool_size=30):
    """Pick songs whose (valence, energy, tempo) are closest to the emotion's target.

    Uses Euclidean distance on min-max scaled features. (Cosine similarity only
    compares the *direction* of the vectors, so e.g. a medium-energy happy song
    could match "Sad" - distance also respects how high/low each feature is.)
    """
    if emotion not in EMOTION_TO_FEATURES:
        raise ValueError(f"Emotion '{emotion}' is not recognized.")

    target = scaler.transform(pd.DataFrame([EMOTION_TO_FEATURES[emotion]])[FEATURES])
    distances = np.linalg.norm(song_matrix - target, axis=1)
    ranked = songs.iloc[np.argsort(distances)[: pool_size * 3]]
    closest = ranked.drop_duplicates(subset="name").head(pool_size)  # skip covers of the same song
    picked = closest.sample(n=min(num_songs, len(closest)))  # a little variety each time

    results = []
    for _, row in picked.iterrows():
        artists = clean_artists(row["artists"])
        image, url, embed_url = spotify_lookup(row["name"], artists)
        results.append({
            "name": row["name"],
            "artists": artists,
            "year": int(row["year"]),
            "valence": round(float(row["valence"]), 2),
            "energy": round(float(row["energy"]), 2),
            "tempo": round(float(row["tempo"])),
            "image": image,
            "url": url,
            "embed_url": embed_url,
        })
    return results


# ---------------------------------------------------------------- routes
@app.get("/api/health")
def health():
    return jsonify(status="ok", songs=len(songs), spotify=sp is not None)


@app.post("/detect-emotion")
def detect_emotion():
    file = request.files.get("file")
    if file is None:
        return jsonify(error="No file uploaded"), 400
    if file.filename == "":
        return jsonify(error="No selected file"), 400

    try:
        emotion, confidence, face_found, all_probs = predict_emotion(file.read())
    except ValueError as e:
        return jsonify(error=str(e)), 400

    try:
        recommended = recommend_songs(emotion)
    except Exception as e:
        app.logger.exception("Recommendation failed")
        return jsonify(error=f"Something went wrong: {e}"), 500

    return jsonify(
        emotion=emotion,
        confidence=int(round(confidence)),
        face_detected=face_found,
        probabilities=all_probs,
        recommended_songs=recommended,
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify(error=f"Image is too large (max {MAX_UPLOAD_MB} MB)."), 413


# Serve the built React app (frontend/build) if it exists: `npm run build` in frontend/
@app.get("/", defaults={"path": ""})
@app.get("/<path:path>")
def serve_frontend(path):
    build = os.path.abspath(FRONTEND_BUILD)
    if not os.path.isdir(build):
        return jsonify(message="emuziek API is running. Start the React app in frontend/ (npm start)."), 200
    if path and os.path.exists(os.path.join(build, path)):
        return send_from_directory(build, path)
    return send_from_directory(build, "index.html")  # client-side routes like /music-player


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
