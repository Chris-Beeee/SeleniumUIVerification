from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

class AmazonHomePage:
    # --- Locators ---
    URL = "https://www.amazon.co.uk/"
    CAPTCHA_BOX = (By.CSS_SELECTOR, "#captchacharacters")
    COOKIE_BTN = (By.CSS_SELECTOR, "input#sp-cc-accept")
    SEARCH_BOX = (By.CSS_SELECTOR, "input#twotabsearchtextbox")
    PRODUCT_CONTAINER = (By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
    
    # These locators are relative to the PRODUCT_CONTAINER
    TITLE_LINK = (By.CSS_SELECTOR, "h2 span")
    SPONSORED_BADGE = (By.CSS_SELECTOR, ".puis-sponsored-label-text, .s-widget-sponsored-label-text, .puis-label-popover")
    CHOICE_BADGE = (By.CSS_SELECTOR, ".a-badge-label")
    STAR_RATING = (By.CSS_SELECTOR, "span.a-icon-alt")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver, 5)

    # --- Actions ---
    def load(self):
        self.driver.get(self.URL)

    def check_for_captcha(self):
        """Returns True if Amazon blocked us with a CAPTCHA"""
        return len(self.driver.find_elements(*self.CAPTCHA_BOX)) > 0

    def accept_cookies_if_present(self):
        try:
            cookie_btn = self.short_wait.until(EC.element_to_be_clickable(self.COOKIE_BTN))
            cookie_btn.click()
            time.sleep(1)
        except TimeoutException:
            pass

    def search(self, product_name):
        search_box = self.short_wait.until(EC.element_to_be_clickable(self.SEARCH_BOX))
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3) # Wait for results page

    def get_parsed_products(self, limit=15):
        """Returns a list of dictionaries containing rich product data"""
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_CONTAINER))
        containers = self.driver.find_elements(*self.PRODUCT_CONTAINER)
        
        parsed_products = []
        for container in containers[:limit]:
            # Extract Title
            titles = container.find_elements(*self.TITLE_LINK)
            title_text = titles[0].get_attribute("textContent").strip() if titles else "Unknown"
            
            # Extract Sponsored
            sponsored = container.find_elements(*self.SPONSORED_BADGE)
            is_sponsored = True if sponsored else False
            
            # Extract Choice
            choice = container.find_elements(*self.CHOICE_BADGE)
            is_choice = True if choice and "Choice" in choice[0].get_attribute("textContent") else False
            
            # Extract Rating
            stars = container.find_elements(*self.STAR_RATING)
            rating = stars[0].get_attribute("textContent").strip() if stars else "No rating"
            
            parsed_products.append({
                "title": title_text,
                "is_sponsored": is_sponsored,
                "is_choice": is_choice,
                "rating": rating
            })
            
        return parsed_products
