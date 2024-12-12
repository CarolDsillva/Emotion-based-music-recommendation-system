import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import MusicPlayerPage from "./components/MusicPlayerpage";
import MusicRecomendations from "./components/MusicRecomendations";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/music-player" element={<MusicPlayerPage />} />
                <Route path="/music-recommendation" element={<MusicRecomendations />} />
            </Routes>
        </Router>
    );
}

export default App;
