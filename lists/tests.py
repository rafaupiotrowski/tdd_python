from lists.models import Item, List
from lists.views import home_page
from django.urls import resolve
from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class NewListTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post(
		'/lists/new',
		data={'item_text': 'Nowy element listy'}
		)
		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'Nowy element listy')

	def test_redirects_after_POST(self):
		response = self.client.post(
		'/lists/new',
		data={'item_text': 'Nowy element listy'}
		)

		self.assertRedirects(response, '/lists/the_only_list_in_the_world/')

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the_only_list_in_the_world/')
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1', list = list_)
		Item.objects.create(text='itemey 2', list = list_)

		response = self.client.get('/lists/the_only_list_in_the_world/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

class HomePage(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')	
		self.assertEqual(found.func, home_page)

	def test_home_page_uses_correct_template(self):
		c=Client()
		response = c.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

class ListandItemModelsTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'Absolutnie pierwszy element listy'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Drugi element'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(),2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
		self.assertEqual(second_saved_item.text, 'Drugi element')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.list, list_)




