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

class TMDBGenericMoviesPage(BasePage):
    # Matches both the old TMDB UI (h2 a) and the new Tailwind UI (h2.whitespace-normal span)
    MOVIE_TITLES = (By.CSS_SELECTOR, "h2.whitespace-normal span, h2 a")
    ACCEPT_COOKIES_BTN = (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")

    def __init__(self, driver, url):
        # Override init to accept a dynamic URL
        super().__init__(driver)
        self.url = url

    def load(self):
        self.driver.get(self.url)

    def accept_cookies(self):
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable(self.ACCEPT_COOKIES_BTN)
            ).click()
        except Exception:
            pass

    def get_movie_titles(self):
        self.wait_for_presence(*self.MOVIE_TITLES)
        elements = self.driver.find_elements(*self.MOVIE_TITLES)
        titles = [el.text.strip() for el in elements if el.text.strip()]
        return titles

class TMDBDiscoverPage(BasePage):
    URL = "https://www.themoviedb.org/movie"
    
    SEARCH_BUTTON = (By.CSS_SELECTOR, "div.apply.small.background_color.light_blue a")
    MOVIE_TITLES = (By.CSS_SELECTOR, "h2.whitespace-normal span, h2 a")
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
            pass

    def select_show_me(self, option_text):
        locator = (By.XPATH, f"//label[contains(text(), '{option_text}')]")
        self.wait_for_presence(*locator)
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(*locator))

    def toggle_availability(self, option_text):
        locator = (By.XPATH, f"//label[contains(text(), '{option_text}')]")
        self.wait_for_presence(*locator)
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(*locator))

    def select_genre(self, genre_name):
        locator = (By.XPATH, f"//ul[@id='with_genres']/li/a[text()='{genre_name}']")
        self.wait_for_presence(*locator)
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(*locator))

    def set_release_dates(self, start_date, end_date):
        # TMDB's date pickers
        start_locator = (By.CSS_SELECTOR, "input#release_date_gte")
        end_locator = (By.CSS_SELECTOR, "input#release_date_lte")
        self.wait_for_presence(*start_locator)
        
        from selenium.webdriver.common.keys import Keys
        # Use send_keys to trigger JS events properly, clear the field first
        start_el = self.driver.find_element(*start_locator)
        self.driver.execute_script("arguments[0].value = '';", start_el)
        start_el.send_keys(start_date)
        start_el.send_keys(Keys.TAB)
        
        end_el = self.driver.find_element(*end_locator)
        self.driver.execute_script("arguments[0].value = '';", end_el)
        end_el.send_keys(end_date)
        end_el.send_keys(Keys.TAB)

    def add_keyword(self, keyword):
        keyword_input = (By.CSS_SELECTOR, "span.k-multiselect input.k-input-inner")
        self.wait_for_presence(*keyword_input)
        self.set(keyword_input, keyword)
        
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
        time.sleep(1.5) # Wait for autocomplete dropdown
        # Click the exact autocomplete suggestion (case-insensitive)
        xpath = f"//ul[@id='with_keywords_listbox']/li[translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{keyword.lower()}']"
        dropdown_item = (By.XPATH, xpath)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(dropdown_item)).click()

    def set_certifications(self, certs):
        """Selects the specified certifications (e.g. ['PG', '15'])."""
        if not certs:
            return
        for cert in certs:
            locator = (By.XPATH, f"//ul[@id='certification']/li[@data-value='{cert}']")
            self.wait_for_presence(*locator)
            el = self.driver.find_element(*locator)
            classes = el.get_attribute("class") or ""
            if "selected" not in classes:
                self.driver.execute_script("arguments[0].click();", el)

    def set_user_score_range(self, min_score, max_score):
        """Sets the user score range using the Kendo Range Slider widget."""
        self.driver.execute_script(
            """
            var slider = $("#user_score_range").data("kendoRangeSlider");
            if (slider) {
                slider.values(arguments[0], arguments[1]);
                slider.trigger("change");
            } else {
                $("#vote_average_gte").val(arguments[0]);
                $("#vote_average_lte").val(arguments[1]);
            }
            """, min_score, max_score
        )

    def set_minimum_user_votes(self, min_votes):
        """Sets the minimum user votes using the Kendo Slider widget."""
        self.driver.execute_script(
            """
            var slider = $("#user_vote_range").data("kendoSlider");
            if (slider) {
                slider.value(arguments[0]);
                slider.trigger("change");
            } else {
                $("#user_vote_range").val(arguments[0]);
            }
            """, min_votes
        )

    def select_language(self, lang_code):
        """Selects original language by ISO 639-1 code using Kendo DropDownList."""
        self.driver.execute_script(
            """
            var ddl = $("#language").data("kendoDropDownList");
            if (ddl) {
                ddl.value(arguments[0]);
                ddl.trigger("change");
            } else {
                $("#language").val(arguments[0]);
            }
            """, lang_code
        )

    def set_runtime_range(self, min_mins, max_mins):
        """Sets the movie runtime range in minutes using Kendo Range Slider widget."""
        self.driver.execute_script(
            """
            var slider = $("#runtime_range").data("kendoRangeSlider");
            if (slider) {
                slider.values(arguments[0], arguments[1]);
                slider.trigger("change");
            } else {
                $("#with_runtime_gte").val(arguments[0]);
                $("#with_runtime_lte").val(arguments[1]);
            }
            """, min_mins, max_mins
        )

    def set_availabilities(self, types):
        """Configures availabilities checkboxes (e.g. ['flatrate', 'free'])."""
        all_checkbox_locator = (By.CSS_SELECTOR, "input#all_availabilities")
        self.wait_for_presence(*all_checkbox_locator)
        all_el = self.driver.find_element(*all_checkbox_locator)
        is_all_checked = all_el.is_selected()

        if not types:
            if not is_all_checked:
                self.driver.execute_script("arguments[0].click();", all_el)
            return

        if is_all_checked:
            self.driver.execute_script("arguments[0].click();", all_el)

        mapping = {
            "flatrate": "input#ott_monetization_type_flatrate",
            "free": "input#ott_monetization_type_free",
            "ads": "input#ott_monetization_type_ads",
            "rent": "input#ott_monetization_type_rent",
            "buy": "input#ott_monetization_type_buy"
        }

        for m_type, css_sel in mapping.items():
            locator = (By.CSS_SELECTOR, css_sel)
            self.wait_for_presence(*locator)
            el = self.driver.find_element(*locator)
            should_be_checked = (m_type in types)
            if el.is_selected() != should_be_checked:
                self.driver.execute_script("arguments[0].click();", el)

    def apply_filters(self):
        import time
        self.wait_for_presence(*self.SEARCH_BUTTON)
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(*self.SEARCH_BUTTON))
        time.sleep(2) # Wait for movie grid to refresh via AJAX

    def get_movie_titles(self):
        self.wait_for_presence(*self.MOVIE_TITLES)
        elements = self.driver.find_elements(*self.MOVIE_TITLES)
        return [el.text.strip() for el in elements if el.text.strip()]
