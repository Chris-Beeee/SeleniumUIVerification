from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException

class TMDBHomePage(BasePage):
    URL = "https://www.themoviedb.org/"
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")

    def load(self):
        self.driver.get(self.URL)

    def click_login(self):
        self.click(*self.LOGIN_LINK)


class TMDBLoginPage(BasePage):
    USERNAME_FIELD = (By.CSS_SELECTOR, "input#username")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input#password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input#login_button")
    PROFILE_LINK = (By.CSS_SELECTOR, "a[href^='/u/']")

    def login(self, username, password):
        self.set(self.USERNAME_FIELD, username)
        self.set(self.PASSWORD_FIELD, password)
        self.click(*self.LOGIN_BUTTON)

    def is_login_successful(self):
        try:
            self.wait_for_presence(*self.PROFILE_LINK)
            return True
        except TimeoutException:
            return False

class TMDBNowPlayingPage(BasePage):
    URL = "https://www.themoviedb.org/movie/now-playing"
    
    # Matches both the old TMDB UI (h2 a) and the new Tailwind UI (h2.whitespace-normal span)
    MOVIE_TITLES = (By.CSS_SELECTOR, "h2.whitespace-normal span, h2 a")
    # TMDB uses OneTrust for cookies
    ACCEPT_COOKIES_BTN = (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")

    def load(self):
        self.driver.get(self.URL)

    def accept_cookies(self):
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable(self.ACCEPT_COOKIES_BTN)
            ).click()
        except Exception:
            pass  # Banner might not appear, ignore if it doesn't

    def get_movie_titles(self):
        """Scrapes and returns a list of movie titles from the page."""
        self.wait_for_presence(*self.MOVIE_TITLES)
        elements = self.driver.find_elements(*self.MOVIE_TITLES)
        
        # Extract the text and filter out any empty strings
        titles = [el.text.strip() for el in elements if el.text.strip()]
        return titles
