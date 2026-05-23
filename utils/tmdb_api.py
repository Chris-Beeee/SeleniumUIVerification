import os
import requests

MOCK_MOVIES = [
    "The Matrix",
    "Inception",
    "Interstellar",
    "The Dark Knight",
    "Pulp Fiction"
]

def get_now_playing_movies(is_mock=False):
    """
    Fetches the list of 'Now Playing' movies directly from the TMDB API.
    Returns a tuple: (list of movie title strings, boolean indicating if mock data was used).
    """
    if is_mock:
        return MOCK_MOVIES, True
        
    access_token = os.getenv("TMDB_API_READ_ACCESS_TOKEN")
    if not access_token:
        return MOCK_MOVIES, True
        
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
    return [movie['title'] for movie in data.get("results", [])], False


def get_movies_from_api(endpoint, is_mock=False):
    """
    Fetches the list of movies directly from the TMDB API for a specific endpoint.
    Endpoints: 'now_playing', 'popular', 'upcoming', 'top_rated'
    Returns a tuple: (list of movie title strings, boolean indicating if mock data was used).
    """
    if is_mock:
        return MOCK_MOVIES, True
        
    access_token = os.getenv("TMDB_API_READ_ACCESS_TOKEN")
    if not access_token:
        return MOCK_MOVIES, True
        
    url = f"https://api.themoviedb.org/3/movie/{endpoint}"
    # Added region="GB" to match your local IP address where Selenium is running
    params = {"language": "en-US", "page": 1, "region": "GB"}
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    return [movie['title'] for movie in data.get("results", [])], False
