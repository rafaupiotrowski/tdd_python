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
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(' \n')

        #Po odświeżeniu strony głównej zobaczyła komunikat błędu
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'Element listy nie może być pusty')

		#Spróbowała ponownie, wpisując tekst, i wszystko zadziałało
        self.get_item_input_box().send_keys('Kupić mleko\n')
        self.check_for_row_in_list_table('1: Kupić mleko')

		#Przekornie drugi raz spróbowała utworzyć pusty element na liście
        self.get_item_input_box().send_keys(' \n')

		#Na stronie listy otzymała komuninkat jak wcześniej
        self.check_for_row_in_list_table('1: Kupić mleko')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'Element listy nie może być pusty')

		#Element mogła poprawić, wpisując w nim dowolny tekst.
        self.get_item_input_box().send_keys('Zrobić herbatę\n')
        self.check_for_row_in_list_table('1: Kupić mleko')
        self.check_for_row_in_list_table('2: Zrobić herbatę')


