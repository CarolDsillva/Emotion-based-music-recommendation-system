export const getAuthUrl = () => {
    const clientId = "1f35b2325d49492394d29449ecad5656";
    const redirectUri = "http://localhost:3000/music-player";
    const scopes = [
        "streaming",
        "user-read-playback-state",
        "user-modify-playback-state",
    ];

    const authUrl = `https://accounts.spotify.com/authorize?client_id=${clientId}&response_type=token&redirect_uri=${encodeURIComponent(
        redirectUri
    )}&scope=${scopes.join("%20")}`;

    return authUrl;
};

export const getAccessTokenFromUrl = () => {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    return params.get("access_token");
};
