"""
End-to-end browser test: drives the real UI in Chromium.

Prereqs:  the app running (backend on :5000 serving frontend/build, or React on :3000)
          pip install playwright && python -m playwright install chromium
Run:      python tests/e2e_test.py [http://127.0.0.1:5000]
Screenshots are saved to tests/screenshots/.
"""
import os
import sys

from playwright.sync_api import expect, sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000"
HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "..", "backend", "sample_images", "fer_sad_sample.jpg")
SHOTS = os.path.join(HERE, "screenshots")
os.makedirs(SHOTS, exist_ok=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))

        # 1. Landing page loads
        page.goto(URL)
        expect(page.get_by_text("Discover Music")).to_be_visible()
        page.screenshot(path=os.path.join(SHOTS, "1_landing.png"))
        print("PASS landing page loads")

        # 1b. Subscribe link + developed-by watermark on the landing page
        sub = page.get_by_role("link", name="Subscribe to my channel")
        expect(sub).to_be_visible()
        expect(sub).to_have_attribute("href", "https://www.youtube.com/@CarolDsillva?sub_confirmation=1")
        expect(page.get_by_text("Developed by Carol Dsilva")).to_be_visible()
        print("PASS subscribe link + watermark on landing page")

        # 2. Clicking Detect without an image shows a friendly error
        page.get_by_role("button", name="Detect Emotion").click()
        expect(page.get_by_role("alert")).to_contain_text("Please upload or capture an image")
        print("PASS error shown when no image selected")

        # 3. Upload a face photo -> results page
        page.set_input_files("#image-upload", SAMPLE)
        page.get_by_role("button", name="Detect Emotion").click()
        page.wait_for_url("**/music-player", timeout=60_000)
        expect(page.locator(".emotion-result")).to_contain_text("Sad")
        cards = page.locator(".song-card")
        expect(cards).to_have_count(6)
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(SHOTS, "2_results.png"), full_page=True)
        print("PASS emotion detected (Sad) and 6 songs recommended")
        expect(page.get_by_role("link", name="Subscribe to my channel")).to_be_visible()
        expect(page.get_by_text("Developed by Carol Dsilva")).to_be_visible()
        print("PASS subscribe link + watermark on results page")

        # 4. Playlist embed set for the emotion
        src = page.locator("#spotify-player").get_attribute("src")
        assert src and "open.spotify.com/embed/playlist/" in src, src
        print("PASS mood playlist embedded")

        # 5. Back to home
        page.get_by_text("Detect Again").click()
        expect(page.get_by_text("Discover Music")).to_be_visible()
        print("PASS 'Detect Again' returns home")

        assert not errors, f"JavaScript errors: {errors}"
        print("PASS no JavaScript errors")
        browser.close()
    print("\nALL E2E CHECKS PASSED")


if __name__ == "__main__":
    main()
