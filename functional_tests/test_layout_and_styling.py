from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

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

