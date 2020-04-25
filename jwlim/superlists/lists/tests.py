import re
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page


def remove_csrf(html_code):
    csrf_regex = r'<[^<]*csrfmiddlewaretoken[^>]*>'
    return re.sub(csrf_regex, '', html_code)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(remove_csrf(response.content.decode()), remove_csrf(expected_html))

    def test_home_page_can_save_a_POST_request(self):
        # Setup
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        # Exercise
        response = home_page(request)

        # Assert
        self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': '신규 작업 아이템'}
        )
        self.assertEqual(remove_csrf(response.content.decode()), remove_csrf(expected_html))
