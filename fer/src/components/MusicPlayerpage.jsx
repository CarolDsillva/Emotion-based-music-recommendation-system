import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
import spotifyConfig from "../spotifyConfig";
import "./MusicPlayer.css"

const MusicPlayerPage = () => {
    const location = useLocation();
    const { emotion, confidence} = location.state || {};

    useEffect(() => {
        if (!emotion) {
            console.error("No emotion detected.");
            return;
        }

        const playlistId = spotifyConfig.playlists[emotion];
        if (playlistId) {
            const embedUrl = `https://open.spotify.com/embed/playlist/${playlistId}`;
            document.getElementById("spotify-player").src = embedUrl;
        }
    }, [emotion]);

    return (
        <div className="landing-container">
            <h1 className="headinf">Your Personalized Playlist</h1>
            <p className="emotion-result">Predicted Emotion: {emotion}</p>
            <p>Confidence: {confidence}%</p>
            <iframe
                id="spotify-player"
                src=""
                width="100%"
                height="600px"
                frameBorder="0"
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                className="player"
                title="Spotify Player"
            ></iframe>
        </div>
    );
};

export default MusicPlayerPage;
