import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class GiantBombAPIClient:
    """
    Simulates or calls the official Giant Bomb API.
    If GIANTBOMB_API_KEY is present in the environment/dot-env, it will perform real HTTP requests.
    Otherwise, it falls back to a realistic mock response dataset.
    """
    API_URL = "https://www.giantbomb.com/api/videos/"

    def __init__(self):
        self.api_key = os.getenv("GIANTBOMB_API_KEY")
        self.is_mock = not bool(self.api_key)

    def get_recent_videos(self, limit=15) -> list[str]:
        """
        Retrieves recent video titles from the Giant Bomb backend API.
        
        :param limit: Maximum number of titles to return
        :return: A list of video title strings
        """
        if not self.is_mock:
            print(f"[API CLIENT] Calling real Giant Bomb API...")
            try:
                # Giant Bomb API requires a custom User-Agent and key
                headers = {
                    "User-Agent": "SeleniumTestSuite/1.0 (Portfolio Automation Stack)"
                }
                params = {
                    "api_key": self.api_key,
                    "format": "json",
                    "limit": limit,
                    "field_list": "name"
                }
                response = requests.get(self.API_URL, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    titles = []
                    for item in data.get("results", []):
                        name = item.get("name", "")
                        if name:
                            titles.append(name)
                    return titles
                else:
                    print(f"[API CLIENT] Real Giant Bomb API failed with status code {response.status_code}. "
                          f"Falling back to mock data.")
            except Exception as e:
                print(f"[API CLIENT] Exception while calling Giant Bomb API: {e}. Falling back to mock data.")

        # Default Mock Fallback Mode
        # These are structured to contain classic / semi-permanent GiantBomb shows
        # and recent releases that often appear on the homepage.
        print(f"[API CLIENT] Running in Mock Fallback Mode. Returning static simulated backend dataset...")
        return [
            "Bully | Endurance Run: Episode 08",
            "Quick Look at Lego Batman: Legacy of the Dark Knight",
            "Giant Bomb's Donkey Kong 64 Sub-A-Thon: Day 5",
            "Grubbsnax Premium Episode 012",
            "Game Mess Mornings: 5/18/26",
            "9 Lives of Mister Mistofelees: Episode 08",
            "Voicemail Dump Truck: Episode 112",
            "UPF: Unprofessional Fridays",
            "Quick Look: Harold Halibut",
            "Game Mess Mornings: Summer Game Fest Predictions",
            "Giant Bombcast: The Game of the Year Special",
            "Albummer! Episode 80: Metallica's Lulu",
            "Very Online Show: The Mystery of the TikTok Algorithm",
            "Quick Look: Pacific Drive",
            "Unprofessional Fridays: The Spring Special"
        ][:limit]
