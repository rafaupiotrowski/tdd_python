from django.urls import resolve
from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePage(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')	
		self.assertEqual(found.func, home_page)

	def test_home_page_uses_correct_template(self):
		c=Client()
		response = c.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'Nowy element listy'

		response=home_page(request)

		self.assertIn('Nowy element listy', response.content.decode())
		expected_html = render_to_string(
			'home.html', {'new_item_text': 'Nowy element listy'}
		)
