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

		#Po odświeżeniu strony głównej zobaczyła komunikat błędu

		#Spróbowała ponownie, wpisując tekst, i wszystko zadziałało

		#Przekornie drugi raz spróbowała utworzyć pusty element na liście

		#Na stronei listy otzymała komuninkat jak wcześniej

		#Element mogła poprawić, wpisując w nim dowolny tekst.
		self.fail('Napisz mnie')

#		self.fail('Zakończenie testu!')

