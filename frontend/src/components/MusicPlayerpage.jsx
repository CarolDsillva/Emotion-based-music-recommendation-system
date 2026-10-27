/*
 * emuziek - Developed by Carol Dsilva
 * YouTube: https://www.youtube.com/@CarolDsillva
 */
import React, { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./MusicPlayer.css";
import CreatorBadge from "./CreatorBadge";
import spotifyConfig from "../spotifyConfig";

const MusicPlayerPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { emotion, confidence, faceDetected, recommendedSongs = [] } = location.state || {};

  useEffect(() => {
    if (!emotion) {
      console.error("No emotion detected.");
      return;
    }

    const playlistId = spotifyConfig.playlists[emotion];
    if (playlistId) {
      const embedUrl = `https://open.spotify.com/embed/playlist/${playlistId}?utm_source=generator&theme=0`;
      document.getElementById("spotify-player").src = embedUrl;
    }
  }, [emotion]);

  const handleBackToHome = () => {
    navigate("/"); // Navigate back to the landing page
  };

  return (
    <div className="landing-container">
      <nav className="navbar">
        <h2>🎵 emuziek</h2>
        <button onClick={handleBackToHome} className="back-button">
          &#8592; Detect Again
        </button>
        
      </nav>
      <p className="emotion-result">
            Predicted Emotion: <strong>{emotion}</strong> with Probability: <strong> {confidence}%</strong>
          </p>
      {faceDetected === false && (
        <p className="face-warning">No face found in the photo, so the whole image was used. A clear, front-facing photo works best.</p>
      )}
      <div className="recommendations-container">
        <div className="recommended-songs">
          <h1 className="heading">Recommended Music</h1>
          


          <div className="recommendation-cards">
  {recommendedSongs.length > 0 ? (
    recommendedSongs.map((song, index) => (
      <div key={index} className="song-card">
        {song.image && (
          <img
            src={song.image}
            alt={`Album art for ${song.name}`}
            className="album-art"
          />
        )}
        {song.embed_url && (
          <iframe
            src={song.embed_url}
            width="100%"
            height="80px"
            frameBorder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            title={`Spotify player for ${song.name}`}
            className="player"
          ></iframe>
        )}
        <h3>{song.name}</h3>
        <p>
          <strong>Artist:</strong> {song.artists}
        </p>
        
        <br/>
        <p>
          <strong>Recommendation Criteria</strong>
        </p>
        <p>
          <strong>Valence:</strong> {song.valence}
        </p>
        <p>
          <strong>Tempo:</strong> {song.tempo} BPM
        </p>
        <p>
          <strong>Energy:</strong> {song.energy}
        </p>
        
      </div>
    ))
  ) : (
    <p>No recommended songs available. Try another picture or emotion!</p>
  )}
</div>

        </div>

        <div className="recommended-playlists">
          <h1 className="heading">Recommended Playlist</h1>
          
          <iframe
            id="spotify-player"
            src=""
            width="100%"
            height="1200px"
            frameBorder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            className="player"
            title="Spotify Player"
          ></iframe>
        </div>
      </div>
      <CreatorBadge />
    </div>
  );
};

export default MusicPlayerPage;
