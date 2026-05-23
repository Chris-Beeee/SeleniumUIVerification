import os
import requests
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from pages.tmdb_pages import TMDBHomePage, TMDBLoginPage

# Load the environment variables from the .env file
load_dotenv()

def verify_api_access(token):
    """Makes a request to the TMDB API to verify the access token is valid."""
    url = "https://api.themoviedb.org/3/authentication"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200 and response.json().get("success"):
        print("\nAPI Login successful! Token is valid.")
        return True
    else:
        print(f"\nAPI Login failed! Status Code: {response.status_code}, Response: {response.text}")
        return False

def test_tmdb_login_pom(is_mock_mode):
    if is_mock_mode:
        pytest.skip("Skipping login tests because --mock-api flag is active.")
    # Load credentials from environment
    username = os.getenv("TMDB_USERNAME")
    password = os.getenv("TMDB_PASSWORD")
    access_token = os.getenv("TMDB_API_READ_ACCESS_TOKEN")
    
    if not username or not password or not access_token:
        pytest.fail("TMDB credentials not found in environment variables.")

    # 1. Verify API Login first (Backend verification)
    if not verify_api_access(access_token):
        pytest.fail("TEST FAILED: API token authentication failed.", pytrace=False)

    # 2. Proceed with UI Login
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # Navigate to TMDB and go to login page
        home_page = TMDBHomePage(driver)
        home_page.load()
        home_page.click_login()
        
        # Perform login
        login_page = TMDBLoginPage(driver)
        login_page.login(username, password)
        
        # Verify successful UI login
        if not login_page.is_login_successful():
            pytest.fail("TEST FAILED: Incorrect credentials or UI login took too long.", pytrace=False)
            
        print("\nUI Login successful!")
        
    finally:
        driver.quit()
