from selenium import webdriver
import sys
from django.test import LiveServerTestCase

class FunctionalTest(LiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.server_url = 'http://rafalpiotrowski.com.pl'

	@classmethod
	def tearDownClass(cls):
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


