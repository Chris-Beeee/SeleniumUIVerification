from selenium.webdriver.common.by import By
from .base_page import BasePage

class GiantBombPage(BasePage):
    URL = "http://giantbomb.com"
    
    # Locators
    POPUP_BTN_1 = (By.CSS_SELECTOR, ".cm-btn.cm-btn-success.cm-btn-accept-all")
    POPUP_BTN_2 = (By.CSS_SELECTOR, ".cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes")
    
    # Target element classes from the original test
    TARGET_CLASSES = "hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-orange-500"
    TARGET_CSS = "." + TARGET_CLASSES.replace(":", r"\:").replace(" ", ".")
    TARGET_ELEMENT = (By.CSS_SELECTOR, TARGET_CSS)

    def open(self):
        self.driver.get(self.URL)

    def dismiss_popups(self):
        try:
            popup_btn = self.wait_for_clickable(*self.POPUP_BTN_1)
            self.driver.execute_script("arguments[0].click();", popup_btn)
        except Exception:
            pass
            
        try:
            popup_btn_2 = self.wait_for_clickable(*self.POPUP_BTN_2)
            self.driver.execute_script("arguments[0].click();", popup_btn_2)
        except Exception:
            pass

    def click_target_element(self):
        # Wait for existence/clickability
        self.wait_for_clickable(*self.TARGET_ELEMENT)
        
        # Fresh grab to avoid stale element reference
        fresh_element = self.find(*self.TARGET_ELEMENT)
        self.driver.execute_script("arguments[0].click();", fresh_element)
