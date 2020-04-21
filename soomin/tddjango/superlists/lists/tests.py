from django.urls import reverse, resolve
from django.test import TestCase
from django.http import HttpRequest
from .views import home_page


class HomePageTest(TestCase):

    # 홈페이지 url 설정 확인
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")  # 책과 다르게 reverse. 변경되었다.
        self.assertEqual(found.func, home_page)  # homepage 와 맞는지 check

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        # self.assertTrue(response.content.startswith(b"<html>"))
        # self.assertIn(b"<title>To-do lists</title>", response.content)
        # self.assertTrue(response.content.strip().endswith(b"</html>"))
        # refactoring
        expected_html = render_to_string("home.html")
        self.assertEqual(response.content.decode(), expected_html)
