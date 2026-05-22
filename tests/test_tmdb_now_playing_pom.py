import pytest
from selenium import webdriver
from dotenv import load_dotenv

from pages.tmdb_pages import TMDBNowPlayingPage
from utils.tmdb_api import get_now_playing_movies
from utils.backend_verifier import verify_scraped_against_backend

load_dotenv()

def test_tmdb_now_playing_verification():
    # 1. Fetch backend expected data via API
    try:
        backend_titles = get_now_playing_movies()
        print(f"\n[API] Successfully retrieved {len(backend_titles)} 'Now Playing' movies from the backend.")
    except Exception as e:
        pytest.fail(f"TEST FAILED: Could not fetch from API. Error: {str(e)}", pytrace=False)

    # 2. Scrape the UI via Selenium POM
    scraped_titles = []
    ui_error = None
    
    try:
        driver = webdriver.Chrome()
        try:
            driver.maximize_window()
            now_playing_page = TMDBNowPlayingPage(driver)
            now_playing_page.load()
            now_playing_page.accept_cookies()
            
            scraped_titles = now_playing_page.get_movie_titles()
            print(f"[UI] Successfully scraped {len(scraped_titles)} movie titles from the web page.")
        finally:
            driver.quit()
    except Exception as e:
        from selenium.common.exceptions import TimeoutException
        if isinstance(e, TimeoutException):
            ui_error = "TimeoutException: Selenium timed out. The movie titles never appeared on screen, or the page took too long to load."
        else:
            error_msg = str(e).split('Stacktrace:')[0].strip()
            ui_error = f"{type(e).__name__}: {error_msg}"
        
    # Fail outside the try block to avoid Python exception chaining
    if ui_error:
        pytest.fail(f"TEST FAILED: Selenium encountered an error during UI setup or scraping. Details: {ui_error}", pytrace=False)

    if not scraped_titles:
        pytest.fail("TEST FAILED: Could not scrape any movie titles from the UI.", pytrace=False)

    # 3. Verify that the UI titles match the Backend titles
    # We use the existing verification utility which allows for fuzzy matching 
    # to account for slight UI formatting differences.
    try:
        verify_scraped_against_backend(scraped_titles, backend_titles, is_mock=False, threshold=0.6)
    except AssertionError as e:
        pytest.fail(str(e), pytrace=False)
