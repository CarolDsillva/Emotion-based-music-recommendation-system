import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css";

const LandingPage = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [confirmationMessage, setConfirmationMessage] = useState("");
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
            navigate("/music-player", { state: { emotion: data.emotion, confidence: data.confidence } });
        } catch (error) {
            
            console.error("Error detecting emotion:", error);
        }
    };

    return (
        <div className="landing-container">
            <h2>🎵 emuziek</h2>
            <h1 className="hero-text">Discover the Music That Matches Your Mood</h1>
            <p className="sub-text">
                Let emuziek analyze your emotions and deliver personalized playlists crafted just for you. Experience music that understands you.
            </p>
            <div className="upload-container">
                <input type="file" id="image-upload" onChange={handleImageUpload} />
                <button onClick={handleTakePicture}>Take Picture</button>
                <button onClick={handleDetectEmotion}>Detect My Emotion</button>
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
