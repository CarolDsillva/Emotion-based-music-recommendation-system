import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import MusicPlayerPage from "./components/MusicPlayerpage";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/music-player" element={<MusicPlayerPage />} />
            </Routes>
        </Router>
    );
}

export default App;
