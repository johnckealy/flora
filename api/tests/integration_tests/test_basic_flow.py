from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import os

# Create your tests here.
class AuthTest(LiveServerTestCase):

    def setUp(self) -> None:
        options = Options()
        self.base_url = os.environ.get('ORIGIN_URL', 'https://flora.johnkealy.com')
        if os.environ.get('ENVIRONMENT') == 'dev':
            options.binary_location = '/usr/bin/brave-browser'
        options.headless = True
        options.add_argument('ignore-certificate-errors')
        self.selenium = webdriver.Chrome(options = options)

        return super().setUp()


    def tearDown(self) -> None:
        self.selenium.quit()

        return super().tearDown()


    def test_basic_flow(self):
        """The basic flow involves logging in and creating a
        new device entry."""
        self.selenium.get(self.base_url)
        login_btn = self.selenium.find_element_by_id('login-button')
        login_btn.click()

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "email-input")))

        # fill in login details and submit
        self.selenium.find_element_by_id('email-input').send_keys("guest@email.com")
        self.selenium.find_element_by_id('password-input').send_keys("secret")
        self.selenium.find_element_by_id('submit-login').click()

        WebDriverWait(self.selenium, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "h6")))

        self.selenium.implicitly_wait(20)

        # create a new device entry
        self.selenium.get(self.base_url + '/add-plants')
        self.assertIn("Find your plant", self.selenium.page_source)

        expansion_element = WebDriverWait(self.selenium, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "q-item__label")))

        self.selenium.implicitly_wait(20)
        expansion_element.click()

        radio_elements = WebDriverWait(self.selenium, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "q-radio")))

        self.selenium.implicitly_wait(20)
        radio_elements[2].click()
        self.selenium.implicitly_wait(20)

        self.selenium.find_element_by_id("step1-submit").click()

        roman_text = WebDriverWait(self.selenium, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "roman")))

        plant_heading = roman_text.text
        self.assertIn("Generic High-Light Plant", plant_heading)

        self.selenium.find_element_by_id("nickname").send_keys("Robert Plant")
        self.selenium.find_element_by_id("room").send_keys("Sunroom")
        self.selenium.find_element_by_id("thingspeak-id").send_keys("1193747")
        self.selenium.find_element_by_id("step2-submit").click()

        self.assertIn("Confirm Your Plant", self.selenium.page_source)

        self.selenium.find_element_by_id("step3-submit").click()

        self.assertIn("Robert Plant", self.selenium.page_source)

        self.selenium.close()
