from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class HerokuAppLoginPage(BasePage):
    URL = "https://the-internet.herokuapp.com/login"
    
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.set(self.USERNAME_FIELD, username)
        self.set(self.PASSWORD_FIELD, password)
        self.click(*self.LOGIN_BUTTON)

    def get_flash_message(self):
        return self.get_text(*self.FLASH_MESSAGE)


class HerokuAppDropdownPage(BasePage):
    URL = "https://the-internet.herokuapp.com/dropdown"
    DROPDOWN = (By.ID, "dropdown")

    def open(self):
        self.driver.get(self.URL)

    def select_option(self, visible_text):
        dropdown_element = self.find(*self.DROPDOWN)
        select = Select(dropdown_element)
        select.select_by_visible_text(visible_text)

    def get_selected_option(self):
        dropdown_element = self.find(*self.DROPDOWN)
        select = Select(dropdown_element)
        return select.first_selected_option.text


class HerokuAppAlertPage(BasePage):
    URL = "https://the-internet.herokuapp.com/javascript_alerts"
    JS_ALERT_BTN = (By.XPATH, "//button[text()='Click for JS Alert']")
    RESULT_TEXT = (By.ID, "result")

    def open(self):
        self.driver.get(self.URL)

    def trigger_alert(self):
        self.click(*self.JS_ALERT_BTN)

    def get_alert_text_and_accept(self):
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text

    def get_result_text(self):
        return self.get_text(*self.RESULT_TEXT)


class HerokuAppHoverPage(BasePage):
    URL = "https://the-internet.herokuapp.com/hovers"
    USER_AVATAR = (By.CSS_SELECTOR, ".figure")
    HIDDEN_TEXT = (By.CSS_SELECTOR, ".figcaption h5")

    def open(self):
        self.driver.get(self.URL)

    def get_avatar_element(self):
        return self.find(*self.USER_AVATAR)

    def get_hidden_text_element(self):
        # Using a direct find here because it might not be visible yet
        avatar = self.get_avatar_element()
        return avatar.find_element(*self.HIDDEN_TEXT)

    def hover_over_avatar(self):
        avatar = self.get_avatar_element()
        actions = ActionChains(self.driver)
        actions.move_to_element(avatar).perform()


class HerokuAppDynamicLoadingPage(BasePage):
    URL = "https://the-internet.herokuapp.com/dynamic_loading/2"
    START_BTN = (By.CSS_SELECTOR, "#start button")
    FINISH_TEXT = (By.CSS_SELECTOR, "#finish h4")

    def open(self):
        self.driver.get(self.URL)

    def start_loading(self):
        self.click(*self.START_BTN)

    def get_finish_text(self):
        return self.get_text(*self.FINISH_TEXT)
