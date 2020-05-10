from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape

from django.template.loader import render_to_string
import re

from lists.models import Item, List
from lists.views import home_page


def remove_csrf_tag(text):
    return re.sub(r"<[^>]*csrfmiddlewaretoken[^>]*>", "", text)


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        # self.assertEqual(response.content.decode(), expected_html)
        self.assertEqual(
            remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html)
        )


class ListViewTest(TestCase):
    def test_displays_all_list_items(self):
        list_ = List.objects.create()
        response = self.client.get("/lists/%d/" % (list_.id,))
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="다른 목록 아이템 1", list=other_list)
        Item.objects.create(text="다른 목록 아이템 2", list=other_list)

        response = self.client.get("/lists/%d/" % (correct_list.id,))

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "다른 목록 아이템 1")
        self.assertNotContains(response, "다른 목록 아이템 2")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id, ))
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "신규 작업 아이템"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "신규 작업 아이템")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "신규 작업 아이템"})
        new_list = List.objects.first()
        self.assertRedirects(response, "/lists/%d/" % (new_list.id,))

    def test_validation_errors_are_sent_back_to_home_pate_tempalate(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            "/lists/%d/add_item" % (correct_list.id,),
            data={"item_text": "기존 목록에 신규 아이템"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "기존 목록에 신규 아이템")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            "/lists/%d/add_item" % (correct_list.id,),
            data={"item_text": "기존 목록에 신규 아이템"},
        )

        self.assertRedirects(response, "/lists/%d/" % (correct_list.id))
