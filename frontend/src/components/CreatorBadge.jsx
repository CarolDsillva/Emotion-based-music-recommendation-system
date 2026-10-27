/*
 * emuziek - Developed by Carol Dsilva
 * YouTube: https://www.youtube.com/@CarolDsillva
 *
 * "Subscribe" link + "Developed by" watermark shown on every page.
 */
import React from "react";
import "./CreatorBadge.css";

export const CHANNEL_URL = "https://www.youtube.com/@CarolDsillva";
export const SUBSCRIBE_URL = `${CHANNEL_URL}?sub_confirmation=1`;

const CreatorBadge = () => (
    <footer className="creator-badge" aria-label="Creator">
        <a
            className="subscribe-link"
            href={SUBSCRIBE_URL}
            target="_blank"
            rel="noopener noreferrer"
        >
            <span className="yt-icon" aria-hidden="true">▶</span>
            Subscribe to my channel
        </a>
        <a
            className="developed-by"
            href={CHANNEL_URL}
            target="_blank"
            rel="noopener noreferrer"
        >
            Developed by Carol Dsilva · @CarolDsillva
        </a>
    </footer>
);

export default CreatorBadge;
