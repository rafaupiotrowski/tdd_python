from .base import FunctionalTest
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
import sys
from unittest import skip
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class ItemValidationTest(FunctionalTest):
	
    def test_cannot_add_empty_list_items(self):
        #Edyta przeszła na stronę główną i przypadkowo spróbowała
        # utworzyć pusty element na liście. Nacisnęła enter w pustym polu
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(' \n')

        #Po odświeżeniu strony głównej zobaczyła komunikat błędu
        error = self.get_error_element()
        self.assertEqual(error.text, 'Element listy nie może być pusty.')

		#Spróbowała ponownie, wpisując tekst, i wszystko zadziałało
        self.get_item_input_box().send_keys('Kupić mleko\n')
        self.check_for_row_in_list_table('1: Kupić mleko')

		#Przekornie drugi raz spróbowała utworzyć pusty element na liście
        self.get_item_input_box().send_keys(' \n')

		#Na stronie listy otzymała komuninkat jak wcześniej
        self.check_for_row_in_list_table('1: Kupić mleko')
        error = self.get_error_element()
        self.assertEqual(error.text, 'Element listy nie może być pusty.')

		#Element mogła poprawić, wpisując w nim dowolny tekst.
        self.get_item_input_box().send_keys('Zrobić herbatę\n')
        self.check_for_row_in_list_table('1: Kupić mleko')
        self.check_for_row_in_list_table('2: Zrobić herbatę')

    def test_cannot_add_duplicate_items(self):
        #Edyta przeszła na stronę głowną i  zaczęła tworzyć nową lsitę.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Kupić kalosze\n')
        self.check_for_row_in_list_table('1: Kupić kalosze')
        
        #Przypadkowo sprobowała wpisać element, ktory już znajdował się na liście
        self.get_item_input_box().send_keys('Kupić kalosze\n')
        
        #Otrzymała czytelny komunikat błędu
        self.check_for_row_in_list_table('1: Kupić kalosze')
        error = self.get_error_element()
        self.assertEqual(error.text, 'Podany element już istnieje na liście.')
        
    def test_error_message_are_cleared_on_input(self):
        #Edyta utworzyła nową listę w sposob, ktory spowodował powstanie błędu weryfikacji:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(' \n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())
        
        #Rozpoczęła wpisywanie danych w elemencie <input>, aby usunać błąd.
        self.get_item_input_box().send_keys('a')
        
        #Była zadowolona, widząc, że komunikat zniknął.
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
        
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
