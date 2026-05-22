import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class YouTubeAPIClient:
    """
    Simulates or calls the official YouTube Data API v3.
    If YOUTUBE_API_KEY is present in the environment/dot-env, it will perform real HTTP requests.
    Otherwise, it falls back to a realistic mock response dataset.
    """
    API_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.is_mock = not bool(self.api_key)

    def get_trending_videos(self, query="trending", limit=15) -> list[str]:
        """
        Retrieves top video titles from the API backend.
        
        :param query: The search query, defaults to "trending"
        :param limit: Maximum number of titles to return
        :return: A list of video title strings
        """
        if not self.is_mock:
            print(f"[API CLIENT] Calling real YouTube API for query: '{query}'...")
            try:
                params = {
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": limit,
                    "key": self.api_key
                }
                response = requests.get(self.API_URL, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    titles = []
                    for item in data.get("items", []):
                        title = item.get("snippet", {}).get("title", "")
                        if title:
                            titles.append(title)
                    return titles
                else:
                    print(f"[API CLIENT] Real API request failed with status code {response.status_code}. "
                          f"Falling back to mock data.")
            except Exception as e:
                print(f"[API CLIENT] Exception while calling YouTube API: {e}. Falling back to mock data.")

        # Default Mock Fallback Mode
        print(f"[API CLIENT] Running in Mock Fallback Mode. Returning static simulated backend dataset...")
        return [
            "MrBeast - I Survived 50 Hours In A Wasteland",
            "GTA 6 Official Trailer 1",
            "Minecraft Movie Official Trailer",
            "Nintendo Direct - June 2026 Announcement",
            "MKBHD - The Future of Smartphones",
            "Mark Rober - Surviving the World's Hardest Obstacle Course",
            "Marvel Studios’ Avengers: Doomsday Teaser",
            "Taylor Swift - The Tortured Poets Department Live",
            "Post Malone - I Had Some Help (Feat. Morgan Wallen)",
            "SpaceX Starship Launch Flight 5 Review",
            "How to Learn Python in 2026 - Complete Road Map",
            "Building a Second Brain - Ali Abdaal",
            "Veritasium - The Science of Silence",
            "Lofi Hip Hop Radio 🎧 Beats to Relax/Study to",
            "Everything wrong with Selenium in 2026"
        ][:limit]
