import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css";

const LandingPage = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [confirmationMessage, setConfirmationMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false); // New state for loading
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [isCameraOpen, setIsCameraOpen] = useState(false);
    const navigate = useNavigate();

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedImage(file);
        }
    };

    const handleTakePicture = () => {
        setIsCameraOpen(true);
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then((stream) => {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
            })
            .catch((err) => {
                console.error("Error accessing camera: ", err);
                setIsCameraOpen(false);
            });
    };

    const handleCapture = () => {
        const context = canvasRef.current.getContext("2d");
        context.drawImage(videoRef.current, 0, 0, 300, 300);
        videoRef.current.srcObject.getTracks().forEach((track) => track.stop()); // Stop the video stream
        canvasRef.current.toBlob((blob) => {
            const file = new File([blob], "captured-image.jpg", { type: "image/jpeg" });
            setSelectedImage(file);
            setConfirmationMessage("Image captured successfully!");
            setTimeout(() => setConfirmationMessage(""), 3000); // Hide message after 3 seconds
            setIsCameraOpen(false);
        });
    };

    const handleDetectEmotion = async () => {
        if (!selectedImage) {
            alert("Please upload or capture an image first.");
            return;
        }

        setIsLoading(true); // Start loading

        const formData = new FormData();
        formData.append("file", selectedImage);

        try {
            const response = await fetch("http://127.0.0.1:5000/detect-emotion", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            if (data.error) {
                alert(data.error);
                return;
            }

            // Pass recommended songs in the navigate function
            navigate("/music-player", { state: { emotion: data.emotion, confidence: data.confidence, recommendedSongs: data.recommended_songs } });
        } catch (error) {
            console.error("Error detecting emotion:", error);
        } finally {
            setIsLoading(false); // Stop loading
        }
    };

    return (
        <div className="landing-container">
            {isLoading && (
                <div className="loading-overlay">
                    <div className="loading-spinner"></div>
                    <p>Predicting emotion</p>
                </div>
            )}
            <h2 className="logo-name">🎵 emuziek</h2>
            <p className="top-label">👾 ML Emotion Music Recommender</p>
            <h1 className="hero-text">Discover Music <br /> That Matches Your Mood</h1>
            <p className="sub-text">
                Analyze your emotions, recommend songs and deliver personalized playlists crafted just for you. <br /> Experience music that understands you.
            </p>
            <div className="upload-container">
                <input type="file" id="image-upload" onChange={handleImageUpload} />
                <button onClick={handleTakePicture}>Take Picture</button>
                <button className="detect-button" onClick={handleDetectEmotion}>Detect Emotion</button>
            </div>
            {confirmationMessage && <p className="confirmation-message">{confirmationMessage}</p>}
            {isCameraOpen && (
                <div className="camera-container">
                    <video ref={videoRef} autoPlay className="video-preview"></video>
                    <canvas ref={canvasRef} width="300" height="300" style={{ display: "none" }}></canvas>
                    <button onClick={handleCapture}>Capture</button>
                </div>
            )}
        </div>
    );
};

export default LandingPage;
