from selenium import webdriver
import unittest

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
        self.fail('Zakończenie testu!')

#Od razu zostaje zachęcona, aby wpisać rzecz do zrobienia.

#W polu tekstowym wpisuje 'Kupić pawie pióra' (hobby Edyty
#polega na tworzeniu ozdobnych przynęt).

#Po naciśnięciu klawisza Enter strona została uaktulaniona i wyświetla
#'1: Kupić pawie pióra' jako element listy rzeczy do zrobienia.

#Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
#Edyta wpisała 'Użyć pawich piór do zrobienia przynęty' (Edyta jest niezwykle skrupulatna).

#Strona została ponownie uaktualniona i teraz wyświetla dwa elelementy na liście rzeczy do zrobienia.

#Edyta była ciekwawa, czy witryna zapamięta jej listę. Zwróciła uwagę na wygenerowany dla niej unikatowy adres URL, obok którego znajduje się pewien tekst z wyjaśnieniem

#Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.

#Usatysfakcjonowana kładzie się spać.
if __name__ == '__main__':
	unittest.main(warnings='ignore')
