import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
import spotifyConfig from "../spotifyConfig";

const MusicPlayerPage = () => {
    const location = useLocation();
    const { emotion} = location.state || {};

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
        <div style={styles.container}>
            <h1 style={styles.heading}>Your Personalized Playlist</h1>
            <p className="emotion-result">Predicted Emotion: {emotion}</p>
            {/* <p>Confidence: {confidence}%</p> */}
            <iframe
                id="spotify-player"
                src=""
                width="100%"
                height="380"
                frameBorder="0"
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                style={styles.player}
                title="Spotify Player"
            ></iframe>
        </div>
    );
};

const styles = {
    container: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        background: "linear-gradient(135deg, #6a0dad, #000)",
        color: "white",
        padding: "1rem",
        textAlign: "center",
    },
    heading: {
        fontSize: "2rem",
        marginBottom: "1rem",
    },
    player: {
        borderRadius: "10px",
    },
};

export default MusicPlayerPage;
