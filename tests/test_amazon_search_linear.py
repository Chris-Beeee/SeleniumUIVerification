#This test is designed to see if Amazon can be used for test automation, as it is a very complex site, but an aggressive bot protection logic.
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time


def test_amazon_product_search():
    driver = webdriver.Chrome()

    try:
        # Navigate to Amazon UK
        driver.get("https://www.amazon.co.uk/")

        # 0. Check for CAPTCHA
        # Amazon often instantly redirects Selenium bots to a CAPTCHA page.
        captcha_present = len(driver.find_elements(By.CSS_SELECTOR, "#captchacharacters")) > 0
        if captcha_present:
            pytest.fail("TEST FAILED: Amazon detected the automation and blocked us with a CAPTCHA!", pytrace=False)
        # 1. Handle Cookies
        try:
            cookie_accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input#sp-cc-accept"))
            )
            cookie_accept.click()
            print("Cookie banner accepted.")
            time.sleep(1)
        except TimeoutException:
            print("No cookie banner appeared.")
        # 2. Find Search Box
        search_box_found = True
        try:
            search_box = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input#twotabsearchtextbox"))
            )
            print("Found search box. Searching for 'monitor'...")
            search_box.send_keys("monitor")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)  # Wait for results page to load
        except TimeoutException:
            search_box_found = False

        if not search_box_found:
            pytest.fail("TEST FAILED: Could not find the Amazon search box.", pytrace=False)

        print("-" * 50)
        # 3. Extract Products and Categories
        print("-" * 50)

        # We look for the main container that holds the entire product card
        product_container_selector = 'div[data-component-type="s-search-result"]'

        products_found = True
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, product_container_selector))
            )
        except TimeoutException:
            products_found = False

        if not products_found:
            pytest.fail("TEST FAILED: Could not find any product containers.", pytrace=False)

        # Grab all the product containers on the page
        product_containers = driver.find_elements(By.CSS_SELECTOR, product_container_selector)

        print(f"Found {len(product_containers)} products. Here is the breakdown:")

        for index, container in enumerate(product_containers[:15], 1):
            # --- Extract Title ---
            # We use .find_elements (plural) so it doesn't crash if a title is missing
            titles = container.find_elements(By.CSS_SELECTOR, "h2 span")
            title_text = titles[0].get_attribute("textContent").strip() if titles else "Unknown Title"

            # --- Extract Sponsored Status ---
            # If the sponsored label exists inside this container, it's an ad
            sponsored_labels = container.find_elements(By.CSS_SELECTOR, ".puis-sponsored-label-text")
            is_sponsored = "Yes" if sponsored_labels else "No"

            # --- Extract Amazon's Choice ---
            choice_badges = container.find_elements(By.CSS_SELECTOR, ".a-badge-label")
            is_choice = "Yes" if choice_badges and "Choice" in choice_badges[0].text else "No"

            # --- Extract Star Rating ---
            # Ratings are usually stored in hidden text like "4.5 out of 5 stars"
            star_ratings = container.find_elements(By.CSS_SELECTOR, "span.a-icon-alt")
            rating = star_ratings[0].get_attribute("textContent").strip() if star_ratings else "No rating"

            # Print it all out nicely formatted
            print(f"\n{index}. {title_text[:60]}...")  # Truncated title so it's easier to read
            print(f"   | Sponsored: {is_sponsored}")
            print(f"   | Amazon's Choice: {is_choice}")
            print(f"   | Rating: {rating}")

    finally:
        driver.quit()