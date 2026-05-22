# This test is for a user who is not signed in to youtube, meaning there are several steps to get the site to display any videos at all
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

# Import Option 4 Backend Verifier & API Client
from utils.youtube_api import YouTubeAPIClient
from utils.backend_verifier import verify_scraped_against_backend, clean_text

def test_youtube_video_titles():
    # Initialize API Client and fetch backend trending videos
    api_client = YouTubeAPIClient()
    backend_titles = api_client.get_trending_videos(query="trending", limit=15)

    driver = webdriver.Chrome()

    try:
        driver.get("https://www.youtube.com/")

        # 1. Handle Cookies
        try:
            accept_button_selector = 'button[aria-label*="Accept the use of cookies"]'
            cookie_accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, accept_button_selector))
            )
            cookie_accept.click()
            print("Cookie banner found and accepted.")
            time.sleep(1)
        except TimeoutException:
            print("No cookie banner appeared (this is normal depending on region/session).")

        # 2. Find Search Box
        search_selector = 'input[name="search_query"]'
        search_box_found = True

        try:
            search_box = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, search_selector))
            )
            print("Found search box. Searching for 'trending' to bypass history screen...")
            search_box.send_keys("trending")
            search_box.send_keys(Keys.RETURN)

            # Give the heavy YouTube results page a few seconds to start rendering
            time.sleep(3)
        except TimeoutException:
            search_box_found = False

        if not search_box_found:
            pytest.fail(
                f"TEST FAILED: Could not find the YouTube search box using the selector: {search_selector}",
                pytrace=False
            )

        print("-" * 50)
        # 3. Extract Titles
        yt_title_selector = "a#video-title"
        videos_found = True

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, yt_title_selector))
            )
        except TimeoutException:
            videos_found = False

        if not videos_found:
            pytest.fail(
                "TEST FAILED: Could not find any video titles within 10 seconds. Layout may have changed.",
                pytrace=False
            )

        video_elements = driver.find_elements(By.CSS_SELECTOR, yt_title_selector)

        print(f"Found {len(video_elements)} video titles in search results:")
        
        scraped_titles = []
        for index, element in enumerate(video_elements[:15], 1):
            title = element.get_attribute("textContent").strip()
            if title:
                print(f"{index}. {clean_text(title)}")
                scraped_titles.append(title)

        # 4. Backend Verification (Option 4)
        verify_scraped_against_backend(
            scraped_titles=scraped_titles,
            backend_titles=backend_titles,
            is_mock=api_client.is_mock
        )

    finally:
        driver.quit()