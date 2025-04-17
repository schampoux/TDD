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
        # setup 
        list_ = List.objects.create()
        
        # exercise
        response = self.client.get(f"/lists/{list_.id}/")

        # assert
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        # setup
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="other list item 1", list = other_list)
        Item.objects.create(text="other list item 2", list = other_list)

        # exercise
        response = self.client.get(f"/lists/{correct_list.id}/")

        # assert
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

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
        
        new_list = List.objects.first()

        self.assertRedirects(
            response = response, 
            expected_url = f'/lists/{new_list.id}/'
            )

class NewItemTest(TestCase):
    def test_can_save_a_post_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create() 
        
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data = {'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')