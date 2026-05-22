import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Import Option 4 Backend Verifier & API Client
from utils.giantbomb_api import GiantBombAPIClient
from utils.backend_verifier import verify_scraped_against_backend, clean_text

def test_giantbomb_video_titles():
    # Initialize API Client and fetch backend recent videos
    api_client = GiantBombAPIClient()
    backend_titles = api_client.get_recent_videos(limit=15)

    driver = webdriver.Chrome()

    try:
        # Navigate to the URL
        driver.get("https://www.giantbomb.com/")

        # 1. Accept Cookie Banner (OneTrust)
        try:
            cookie_accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))
            )
            cookie_accept.click()
            print("Accepted cookies.")
            time.sleep(1)
        except TimeoutException:
            print("No cookie banner appeared.")

        # 2. Close Marketing/Video Floating Ad
        try:
            video_ad_close = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".universalPlayer_close"))
            )
            video_ad_close.click()
            print("Closed floating video ad.")
        except TimeoutException:
            pass
            
        # 3. Close other potential ad overlays
        try:
            other_ad_close = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#cbb"))
            )
            other_ad_close.click()
        except TimeoutException:
            pass

        print("-" * 50)
        selector = "a[href*='/videos/'][class*='hover:underline']"

        # Check if the element appears, but DON'T raise the failure inside the except block
        videos_found = True
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
        except TimeoutException:
            videos_found = False

        if not videos_found:
            pytest.fail(
                "TEST FAILED: Could not find any video titles within 10 seconds. "
                "The CSS selectors did not match the page content.",
                pytrace=False
            )

        video_elements = driver.find_elements(By.CSS_SELECTOR, selector)

        print(f"Found {len(video_elements)} video titles on the front page:")
        
        scraped_titles = []
        for index, element in enumerate(video_elements, 1):
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