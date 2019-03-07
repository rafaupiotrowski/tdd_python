from lists.models import Item
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
class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'Absolutnie pierwszy element listy'
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Drugi element'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(),2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
		self.assertEqual(second_saved_item.text, 'Drugi element')






