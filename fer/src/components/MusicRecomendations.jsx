// MusicRecommendations.jsx
import React from "react";
import "./MusicRecommendations.css";

const MusicRecomendations = ({ recommendations }) => {
  return (
    <div className="recommendations-container">
      <h1 className="heading">Recommended Songs</h1>
      <div className="cards-wrapper">
        {recommendations.length > 0 ? (
          recommendations.map((song, index) => (
            <div className="song-card" key={index}>
              <h2 className="song-name">{song.name}</h2>
              <p className="artist-name">By: {song.artists}</p>
              <div className="song-features">
                <p>
                  <strong>Valence:</strong> {song.valence.toFixed(2)}
                </p>
                <p>
                  <strong>Energy:</strong> {song.energy.toFixed(2)}
                </p>
                <p>
                  <strong>Tempo:</strong> {song.tempo} BPM
                </p>
              </div>
            </div>
          ))
        ) : (
          <p className="no-songs">No recommendations available. Try another emotion!</p>
        )}
      </div>
    </div>
  );
};

export default MusicRecomendations;
