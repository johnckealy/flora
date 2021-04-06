from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Create your tests here.
class AuthTest(LiveServerTestCase):

    def testform(self):
        options = Options()
        options.binary_location = '/usr/bin/brave-browser'
        options.add_argument('ignore-certificate-errors')

        selenium = webdriver.Chrome(options = options)



        selenium.get('https://127.0.0.1:8080/')

        login_btn = selenium.find_element_by_id('login-button')
        login_btn.click()

        assert "Don't have an account" in selenium.page_source
        selenium.close()