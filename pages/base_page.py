from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, int(os.getenv("IMPLICIT_WAIT", 10)))

    def find(self, *locator):
        return self.driver.find_element(*locator)

    def click(self, *locator):
        self.wait_for_clickable(*locator).click()

    def set(self, locator, value):
        element = self.wait_for_visible(*locator)
        element.clear()
        element.send_keys(value)

    def get_text(self, *locator):
        return self.wait_for_visible(*locator).text

    def wait_for_visible(self, *locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, *locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_presence(self, *locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def get_title(self):
        return self.driver.title
