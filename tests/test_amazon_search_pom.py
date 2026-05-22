#Uitlising the page object model of test creation rather than having all logic within the test case.

import pytest
from selenium import webdriver
from pages.amazon_home import AmazonHomePage


def test_amazon_search():
    driver = webdriver.Chrome()

    try:
        home_page = AmazonHomePage(driver)

        home_page.load()
        if home_page.check_for_captcha():
            pytest.fail("Hit a CAPTCHA wall!", pytrace=False)

        home_page.accept_cookies_if_present()
        home_page.search("monitor")

        results = home_page.get_parsed_products()
        assert len(results) > 0

        # Now you have clean data to work with!
        for item in results:
            print(f"{item['title'][:40]} | Ad? {item['is_sponsored']} | Choice? {item['is_choice']} | Rating: {item['rating']}")

    finally:
        driver.quit()