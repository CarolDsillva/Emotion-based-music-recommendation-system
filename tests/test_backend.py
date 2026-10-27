"""
Backend tests for emuziek.   Run from the repo root:   python -m pytest tests -v

The live Spotify test only runs when SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET are set.
"""
import io
import os
import sys

import cv2
import numpy as np
import pytest

BACKEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
sys.path.insert(0, os.path.abspath(BACKEND))

import app as backend  # noqa: E402  (loads the model + dataset once)

SAMPLE = os.path.join(BACKEND, "sample_images", "fer_sad_sample.jpg")


@pytest.fixture()
def client():
    backend.app.config["TESTING"] = True
    return backend.app.test_client()


@pytest.fixture()
def no_spotify(monkeypatch):
    """Keep tests offline & fast: pretend Spotify returns nothing."""
    monkeypatch.setattr(backend, "spotify_lookup", lambda name, artists: (None, None, None))


def jpg_bytes(img):
    ok, buf = cv2.imencode(".jpg", img)
    assert ok
    return buf.tobytes()


def post_image(client, data, filename="photo.jpg"):
    return client.post(
        "/detect-emotion",
        data={"file": (io.BytesIO(data), filename)},
        content_type="multipart/form-data",
    )


# ------------------------------------------------------------------ startup
def test_model_and_data_loaded():
    assert backend.model.input_shape == (None, 48, 48, 1)
    assert backend.model.output_shape == (None, 7)
    assert len(backend.songs) > 10_000
    assert (backend.songs["popularity"] >= backend.MIN_POPULARITY).all()


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


# ------------------------------------------------------------------ emotion detection
def test_detect_emotion_on_fer_sample(client, no_spotify):
    r = post_image(client, open(SAMPLE, "rb").read())
    assert r.status_code == 200, r.get_json()
    body = r.get_json()
    assert body["emotion"] == "Sad"  # known label of this FER-2013 test image
    assert 0 <= body["confidence"] <= 100
    assert set(body["probabilities"]) == set(backend.EMOTION_LABELS)
    assert abs(sum(body["probabilities"].values()) - 100) < 1
    assert len(body["recommended_songs"]) == 6
    for song in body["recommended_songs"]:
        for key in ["name", "artists", "valence", "energy", "tempo", "image", "url", "embed_url"]:
            assert key in song
        assert "[" not in song["artists"]  # cleaned from "['Artist']"


def test_face_is_found_and_cropped_in_a_larger_photo(client, no_spotify):
    face = cv2.resize(cv2.imread(SAMPLE, cv2.IMREAD_GRAYSCALE), (180, 180))
    canvas = np.full((480, 640), 200, np.uint8)  # plain background around the face
    canvas[150:330, 230:410] = face
    body = post_image(client, jpg_bytes(canvas)).get_json()
    assert body["face_detected"] is True
    assert body["emotion"] in backend.EMOTION_LABELS


def test_photo_without_face_still_works(client, no_spotify):
    blank = np.full((300, 300, 3), 127, np.uint8)
    r = post_image(client, jpg_bytes(blank))
    assert r.status_code == 200
    assert r.get_json()["face_detected"] is False


def test_png_upload(client, no_spotify):
    ok, buf = cv2.imencode(".png", cv2.imread(SAMPLE))
    r = post_image(client, buf.tobytes(), "face.png")
    assert r.status_code == 200


# ------------------------------------------------------------------ bad input
def test_no_file(client):
    r = client.post("/detect-emotion", data={}, content_type="multipart/form-data")
    assert r.status_code == 400
    assert "No file" in r.get_json()["error"]


def test_empty_filename(client):
    r = post_image(client, b"", filename="")
    assert r.status_code == 400


def test_not_an_image(client):
    r = post_image(client, b"this is not an image", "notes.txt")
    assert r.status_code == 400
    assert "Could not read the image" in r.get_json()["error"]


def test_too_large(client):
    r = post_image(client, b"0" * (backend.MAX_UPLOAD_MB * 1024 * 1024 + 10))
    assert r.status_code == 413


# ------------------------------------------------------------------ recommendations
@pytest.mark.parametrize("run", range(5))  # recommendations are random - check several draws
@pytest.mark.parametrize("emotion", list(backend.EMOTION_TO_FEATURES))
def test_recommendations_match_the_mood(emotion, run, no_spotify):
    target = backend.EMOTION_TO_FEATURES[emotion]
    recs = backend.recommend_songs(emotion)
    assert len(recs) == 6
    assert len({s["name"] for s in recs}) == 6  # no duplicate songs (or covers)
    for s in recs:
        assert abs(s["valence"] - target["valence"]) < 0.15, s
        assert abs(s["energy"] - target["energy"]) < 0.15, s
        assert abs(s["tempo"] - target["tempo"]) < 25, s


def test_unknown_emotion():
    with pytest.raises(ValueError):
        backend.recommend_songs("Sleepy")


def test_spotify_errors_do_not_break_the_app(client, monkeypatch):
    class BrokenSpotify:
        def search(self, *a, **k):
            raise ConnectionError("Spotify is down")

    monkeypatch.setattr(backend, "sp", BrokenSpotify())
    r = post_image(client, open(SAMPLE, "rb").read())
    assert r.status_code == 200
    assert all(s["image"] is None for s in r.get_json()["recommended_songs"])


def test_clean_artists():
    assert backend.clean_artists("['Adele']") == "Adele"
    assert backend.clean_artists("['A', 'B']") == "A, B"


# ------------------------------------------------------------------ frontend served by Flask
def test_frontend_or_api_message_at_root(client):
    r = client.get("/")
    assert r.status_code == 200
    build = os.path.join(BACKEND, "..", "frontend", "build", "index.html")
    if os.path.exists(build):
        assert b"<div id=\"root\">" in r.data
        assert client.get("/music-player").status_code == 200  # client-side route
    else:
        assert b"API is running" in r.data


# ------------------------------------------------------------------ live Spotify (optional)
@pytest.mark.skipif(backend.sp is None, reason="Spotify credentials not set")
def test_live_spotify_lookup():
    image, url, embed = backend.spotify_lookup("Blinding Lights", "The Weeknd")
    assert url and url.startswith("https://open.spotify.com/track/")
    assert embed and "/embed/track/" in embed
    assert image and image.startswith("https://")
