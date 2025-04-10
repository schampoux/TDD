from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List 
from rich.traceback import install

install()


class ListViewTest(TestCase):
    def test_uses_list_template(self):

        # exercise
        response = self.client.get("/lists/the-only-list-in-the-world/")

        # assert
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_items(self):
        # setup
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        # exercise
        response = self.client.get("/lists/the-only-list-in-the-world/")

        # assert
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List() 
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        
        self.assertEqual(
            first = saved_list, 
            second = list_ 
        )

        saved_items = Item.objects.all()
        
        self.assertEqual(
            first = saved_items.count(), 
            second = 2
        )

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        
        self.assertEqual(
            first = first_saved_item.text, 
            second = "The first (ever) list item"
        )
        
        self.assertEqual(
            first = first_saved_item.list, 
            second = list_ 
        )
        
        self.assertEqual(
            first = second_saved_item.text, 
            second = "Item the second"
        )

        self.assertEqual(
            first = second_saved_item.list,
            second = list_
        )
        
class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        
        self.client.post(
            path = "/lists/new", 
            data = {"item_text": "A new list item"}
            )
        
        self.assertEqual(
            first = Item.objects.count(), 
            second = 1
            )
        
        new_item = Item.objects.first()
        
        self.assertEqual(
            first = new_item.text, 
            second = "A new list item"
            )

    def test_redirects_after_POST(self):
        
        response = self.client.post(
            path = "/lists/new", 
            data = {"item_text": "A new list item"}
            )
        
        self.assertRedirects(
            response = response, 
            expected_url = '/lists/the-only-list-in-the-world/'
            )
