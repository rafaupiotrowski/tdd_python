from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
import sys
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
	#	for arg in sys.argv:
	#		if 'liveserver' in arg:
	#			cls.server_url = 'http://' +arg.split('=')[1]
	#			return
	#	super().setUpClass()
		cls.server_url = 'http://rafalpiotrowski.com.pl'

	@classmethod
	def tearDownClass(cls):
	#	if cls.server_url ==cls.live_server_url:
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

	def test_can_start_a_list_and_retrive_it_later(self):
		#Edyta dowiedziała się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia.
		#Postanowiła więc przejść na stronę główną tej aplikacji.
		self.browser.get(self.server_url)

		#Zwróciła uwagę, że tytuł strony i nagłówek zawierają słowo Listy.
		self.assertIn('Listy', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('listę', header_text)

		#Od razu zostaje zachęcona, aby wpisać rzecz do zrobienia.
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Wpisz rzecz do zrobienia'
		)

		#W polu tekstowym wpisuje 'Kupić pawie pióra' (hobby Edyty
		#polega na tworzeniu ozdobnych przynęt).
		inputbox.send_keys('Kupić pawie pióra')

		#Po naciśnięciu klawisza Enter strona została uaktulaniona i wyświetla
		#'1: Kupić pawie pióra' jako element listy rzeczy do zrobienia.
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Kupić pawie pióra')
		
		#Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
		#Edyta wpisała 'Użyć pawich piór do zrobienia przynęty' (Edyta jest niezwykle skrupulatna).
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
		inputbox.send_keys(Keys.ENTER)
		#Strona została ponownie uaktualniona i teraz wyświetla dwa elelementy na liście rzeczy do zrobienia.
		self.check_for_row_in_list_table('1: Kupić pawie pióra')
		self.check_for_row_in_list_table('2: Użyć pawich piór do zrobienia przynęty')
		
		#Teraz nowy użytkownik Franek zaczyna korzystać z witryny.
		##Używamy nowej sesji przeglądarki internetowej, aby mieć pewność, że żadne
		##informacje dotyczące Edyty nie zostaną ujawnione, na przykład przez cookies.
		self.browser.quit()
		self.browser = webdriver.Chrome()

		#Franek odwiedza stronę główną.
		#Nie znajduje żadnych śladów listy Edyty.
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Kupić pawie pióra', page_text)
		self.assertNotIn('zrobienie przynęty', page_text)

		#Franek tworzy nową listę, wprowadzając nowy element.
		#Jego lista jest mniej interesująca niż Edyty...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Kupić mleko')
		inputbox.send_keys(Keys.ENTER)

		#Franek otrzymuje unikatowy adres URL prowadzący do listy.
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#Ponownie nie ma żadnego śladu po liście Edyty.
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Kupić pawie pióra', page_text)
		self.assertIn('Kupić mleko', page_text)

		#Usatysfakcjonowani, oboje kładą się spać.
		

		#Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.

		#Usatysfakcjonowana kładzie się spać.

	def test_layout_and_styling(self):
		#Edyta przeszła na stronę główną
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)
		
		#Zauważyła, że pole tekstowe zostało elegancko wyśrodkowane.
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
		inputbox.location['x'] + inputbox.size['width']/2,
		512,
		delta=20
		)
		
		#Edyta utworzyła nową listę i zobaczyła, że pole tekstowe nadal jest wyśrodkowane.
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
		inputbox.location['x'] + inputbox.size['width']/2,
		512,
		delta=20
		)

#		self.fail('Zakończenie testu!')
