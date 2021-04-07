from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# Create your tests here.
class AuthTest(LiveServerTestCase):

    def setUp(self) -> None:
        options = Options()
        self.base_url = os.environ.get('ORIGIN_URL')
        if os.environ.get('ENVIRONMENT') == 'dev':
            options.binary_location = '/usr/bin/brave-browser'
        options.headless = True
        options.add_argument('ignore-certificate-errors')
        self.selenium = webdriver.Chrome(options = options)

        return super().setUp()


    def test_login_page(self):
        self.selenium.get(os.environ.get('ORIGIN_URL'))
        login_btn = self.selenium.find_element_by_id('login-button')
        login_btn.click()
        self.assertIn("Don\'t have an account", self.selenium.page_source)
        self.selenium.close()