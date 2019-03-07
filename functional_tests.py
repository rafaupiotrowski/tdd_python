from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrive_it_later(self):
		#Edyta dowiedziała się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia.
		#Postanowiła więc przejść na stronę główną tej aplikacji.
		self.browser.get('http://localhost:8000')

		#Zwróciła uwagę, że tytuł strony i nagłówek zawierają słowo Listy.
		self.assertIn('Listy', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('lista', header_text)

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

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Kupić pawie pióra', [row.text for row in rows])
		#Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
		#Edyta wpisała 'Użyć pawich piór do zrobienia przynęty' (Edyta jest niezwykle skrupulatna).
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
		inputbox.send_keys(Keys.ENTER)
		#Strona została ponownie uaktualniona i teraz wyświetla dwa elelementy na liście rzeczy do zrobienia.
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Kupić pawie pióra', [row.text for row in rows])
		self.assertIn('2: Użyć pawich piór fo zrobienia przynęty', [row.text for row in rows])
		#Edyta była ciekwawa, czy witryna zapamięta jej listę. Zwróciła uwagę na wygenerowany dla niej unikatowy adres URL, obok którego znajduje się pewien tekst z wyjaśnieniem
		self.fail('Zakończenie testu!')

		#Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.

		#Usatysfakcjonowana kładzie się spać.
if __name__ == '__main__':
	unittest.main(warnings='ignore')
