from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class GiantBombHomePage:
    # --- Locators (CSS Selectors) ---
    URL = "https://www.giantbomb.com/"
    COOKIE_ACCEPT_BTN = (By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
    FLOATING_AD_CLOSE_BTN = (By.CSS_SELECTOR, ".universalPlayer_close")
    OTHER_AD_CLOSE_BTN = (By.CSS_SELECTOR, "#cbb")
    VIDEO_TITLES = (By.CSS_SELECTOR, "a[href*='/videos/'][class*='hover:underline']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver, 3)

    # --- Actions ---
    def load(self):
        self.driver.get(self.URL)

    def accept_cookies_if_present(self):
        try:
            cookie_btn = self.short_wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN))
            cookie_btn.click()
        except TimeoutException:
            pass # Ignore if it doesn't appear

    def close_ads_if_present(self):
        try:
            ad_btn = self.short_wait.until(EC.element_to_be_clickable(self.FLOATING_AD_CLOSE_BTN))
            ad_btn.click()
        except TimeoutException:
            pass
            
        try:
            other_btn = self.short_wait.until(EC.element_to_be_clickable(self.OTHER_AD_CLOSE_BTN))
            other_btn.click()
        except TimeoutException:
            pass

    def get_video_titles(self):
        """Waits for titles to load and returns them as a clean list of strings"""
        self.wait.until(EC.presence_of_element_located(self.VIDEO_TITLES))
        elements = self.driver.find_elements(*self.VIDEO_TITLES)
        
        titles = []
        for element in elements:
            text = element.get_attribute("textContent").strip()
            if text:
                titles.append(text)
        return titles
