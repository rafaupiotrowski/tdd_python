from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
User = get_user_model()

class MyListsTests(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        self.browser.get(self.live_server_url + '/404_no_such_url')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/'
        ))
        
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        #Edyta jest zalogowanym użytkownikiem
        email = 'kozatdd@gmail.com'
        self.create_pre_authenticated_session(email)
        
        #Przechodzi na stronę głowną i tworzy listę
        self.browser.get(self.live_server_url)
        self.add_list_item('Kupić przynęty')
        self.add_list_item('Zjeść ślimaki')
        first_list_url = self.browser.current_url
        
        #Zauważa link 'Moje listy' po raz pierwszy
        self.browser.find_element_by_link_text('Moje listy').click()
        
        #Zauważa, że jej lista tam jest, nazwa jak pierszy element listy
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Kupić przynęty')    
        )
        
        self.browser.find_element_by_link_text('Kupić przynęty').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )
        
        #Postanawia zacząć kolejną listę, dla sprawdzenia
        self.browser.get(self.live_server_url)
        self.add_list_item('Policzyć krowy')
        second_list_url = self.browser.current_url
        
        #Pod 'Moje listy', pojawia się jej nowa lista
        self.browser.find_element_by_link_text('Moje listy').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Policzyć krowy')
        )
        self.browser.find_element_by_link_text('Policzyć krowy').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )
        
        #Wylogowuje się. Opcja 'Moje listy znika.
        self.browser.find_element_by_link_text('Wyloguj').click()
        self.wait_for( lambda: self.assertEqual(
            self.browser.find_element_by_link_text('My lists'),
            []
        ))