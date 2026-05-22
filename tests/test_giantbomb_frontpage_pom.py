import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# Import the Page Object
from pages.giantbomb_home import GiantBombHomePage

# Import Option 4 Backend Verifier & API Client
from utils.giantbomb_api import GiantBombAPIClient
from utils.backend_verifier import verify_scraped_against_backend, clean_text

def test_giantbomb_video_titles():
    # Initialize API Client and fetch backend recent videos
    api_client = GiantBombAPIClient()
    backend_titles = api_client.get_recent_videos(limit=15)

    # Initialize the driver
    driver = webdriver.Chrome()
    
    try:
        # 1. Initialize the Page Object
        home_page = GiantBombHomePage(driver)
        
        # 2. Interact with the page
        print("Navigating to Giant Bomb...")
        home_page.load()
        
        print("Checking for popups...")
        home_page.accept_cookies_if_present()
        home_page.close_ads_if_present()
        
        # 3. Get the Data
        try:
            titles = home_page.get_video_titles()
        except TimeoutException:
            pytest.fail("TEST FAILED: Could not find video titles. Selectors may have changed.", pytrace=False)
            
        # 4. Assert / Verify UI scraped something
        assert len(titles) > 0, "No video titles were found on the page!"
        
        print(f"\nFound {len(titles)} video titles on the homepage:")
        for index, title in enumerate(titles, 1):
            print(f"{index}. {clean_text(title)}")
            
        # 5. Backend Verification (Option 4)
        verify_scraped_against_backend(
            scraped_titles=titles,
            backend_titles=backend_titles,
            is_mock=api_client.is_mock
        )
            
    finally:
        # Always close the browser
        driver.quit()
