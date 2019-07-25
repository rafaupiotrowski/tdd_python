from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
#from django.test import LiveServerTestCase
import time
from selenium.webdriver.common.keys import Keys
import os
from datetime import datetime
import unittest
import inspect

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)

MAX_WAIT = 20

class FunctionalTest(StaticLiveServerTestCase):
    
    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '%s/%s.%s-window%s-%s' % (
        SCREEN_DUMP_LOCATION,
            self.__class__.__name__,
            self._testMethodName,
            self._windowid,
            timestamp,
        )
    
    def take_screenshot(self):
        filename = self._get_filename()+ '.png'
        print('screenshoting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to ', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)
        
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
    #    self.server_url = 'http://localhost:8000' 

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html
        self.browser.quit()
        super().tearDown()
        
    def _test_has_failed(self):
        # slightly obscure but couldn't find a better way!
        return any(error for (method, error) in self._outcome.errors)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
    
    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() -start_time > MAX_WAIT:
                        raise e
                    print('idę spać...', file=sys.stderr)
                    time.sleep(0.5)
        return modified_fn
    
    @wait
    def wait_for(self, fn):
        return fn()
                
    @wait            
    def wait_to_be_logged_in(self, email):
        print('wait to be logged in', file=sys.stderr)
        self.browser.find_element_by_link_text('Wyloguj')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)
    
    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
        
    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
        
    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows+1
        self.wait_for_row_in_list_table('%s: %s' % (item_number, item_text))
        
    
        
