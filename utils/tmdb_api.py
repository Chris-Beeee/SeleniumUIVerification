import os
import requests

def get_now_playing_movies():
    """
    Fetches the list of 'Now Playing' movies directly from the TMDB API.
    Returns a list of movie title strings.
    """
    access_token = os.getenv("TMDB_API_READ_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("TMDB_API_READ_ACCESS_TOKEN not found in environment variables.")
        
    url = "https://api.themoviedb.org/3/movie/now_playing"
    # Added region="GB" to match your local IP address where Selenium is running
    params = {"language": "en-US", "page": 1, "region": "GB"}
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    return [movie['title'] for movie in data.get("results", [])]
