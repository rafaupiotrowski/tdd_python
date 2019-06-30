from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'kozatdd@gmail.com'
SUBJECT = 'Your login link for superlists'

class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        #Edyta odwiedza stronę superlists i zauważa pierwszy raz okienko "Zaloguj się'.
        #Mowi jej żeby wpisała swoj email, więc to robi.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
        
        #Pojawia się wiadomość, że email został wysłany
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))
        
        #Sprawdza email i znajduje wiadomość
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        
        #Jest w niej link url
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        
        #klika w niego
        self.browser.get(url)
        
        #jest zalogowana!
        self.wait_to_be_logged_in(email=TEST_EMAIL)
        
        #wylogowuje się
        self.browser.find_element_by_link_text('Wyloguj').click()
        
        #jest wylogowana
        self.wait_to_be_logged_out(email=TEST_EMAIL)
        
        
        
        