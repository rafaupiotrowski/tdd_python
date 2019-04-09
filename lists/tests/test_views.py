from lists.models import Item, List
from lists.views import home_page
from lists.forms import ItemForm
from django.urls import resolve
from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'Nowy element listy'}
        )
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element listy')

    def test_redirects_after_POST(self):
            response = self.client.post(
                '/lists/new',
                data={'text': 'Nowy element listy'}
                )
            new_list = List.objects.first()
            self.assertRedirects(response, '/lists/%d/' % (new_list.id))
	
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = 'Element nie może być pusty'
        self.assertContains(response, expected_error)
	
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')
        
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list = correct_list)
        Item.objects.create(text='itemey 2', list = correct_list)

        other_list = List.objects.create()

        Item.objects.create(text='Element pierwszy innej listy', list = other_list)
        Item.objects.create(text='Element drugi innej listy', list = other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'Element pierwszy innej listy')
        self.assertNotContains(response, 'Element drugi innej listy')
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
                '/lists/%d/' % (correct_list.id),
                data = {'text': 'Nowy element dla istniejącej listy'}
                )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element dla istniejącej listy')
        self.assertEqual(new_item.list, correct_list)      
        
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id),
            data = {'text': 'Nowy element dla istniejącej listy'}
            )
		
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id))
        
    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (list_.id),
            data={'text': ''}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = 'Element nie może być pusty'
        self.assertContains(response, expected_error)
        
class HomePage(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')	
        self.assertEqual(found.func, home_page)

    def test_home_page_renders_home_template(self):
        c=Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_home_page_uses_item_forms(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
