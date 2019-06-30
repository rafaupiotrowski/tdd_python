from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import sys
from django.test import LiveServerTestCase
import time

MAX_WAIT = 19

class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server_url = 'http://rafalpiotrowski.com.pl'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
    
    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if (time.time() - start_time) > MAX_WAIT:
                    raise e
                time.sleep(0.5)
                
    def wait_to_be_logged_in(self, email):
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Wyloguj')
        )
        navbar = self.browser.find_element_by_css_selctor('.navbar')
        self.assertIn(email, navbar.text)
        
    def wait_to_be_logged_out(self, email):
                self.wait_for(
            lambda: self.browser.find_element_by_link_text('Wyloguj')
        )
        navbar = self.browser.find_element_by_css_selctor('.navbar')
        self.assertNotIn(email, navbar.text)
        
