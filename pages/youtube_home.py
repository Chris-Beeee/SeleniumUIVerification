from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

class YouTubeHomePage:
    # --- Locators ---
    URL = "https://www.youtube.com/"
    COOKIE_BTN = (By.CSS_SELECTOR, 'button[aria-label*="Accept the use of cookies"]')
    SEARCH_BOX = (By.CSS_SELECTOR, 'input[name="search_query"]')
    VIDEO_TITLES = (By.CSS_SELECTOR, "a#video-title")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver, 5)

    # --- Actions ---
    def load(self):
        self.driver.get(self.URL)

    def accept_cookies_if_present(self):
        try:
            cookie_btn = self.short_wait.until(EC.element_to_be_clickable(self.COOKIE_BTN))
            cookie_btn.click()
            time.sleep(1) # Give dialog time to disappear
        except TimeoutException:
            pass

    def search(self, search_term):
        """Bypasses the empty history screen by searching for a term"""
        search_box = self.short_wait.until(EC.element_to_be_clickable(self.SEARCH_BOX))
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3) # Wait for results page to render

    def get_video_titles(self, limit=15):
        """Waits for titles to load and returns the top results"""
        self.wait.until(EC.presence_of_element_located(self.VIDEO_TITLES))
        elements = self.driver.find_elements(*self.VIDEO_TITLES)
        
        titles = []
        for element in elements:
            text = element.get_attribute("textContent").strip()
            if text:
                titles.append(text)
            # Stop once we have gathered the requested number of valid titles
            if len(titles) == limit:
                break
                
        return titles
