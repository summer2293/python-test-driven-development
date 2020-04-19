from django.urls import reverse, resolve
from django.test import TestCase
from django.http import HttpRequest
from .views import home_page
from django.template.loader import render_to_string


# Create your tests here.

# 이 부분은 책의 django version이 1.7 이고 지금은 3.0.5 라서 수민님의 코드를 인용하였습니다
# 2.0 version 이후부터 url 들고오는 코드 부분들이 바뀌어 졌어요
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') # 책과 다르게 reverse. 변경되었다.
        self.assertEqual(found.func, home_page) # homepage 와 맞는지 check

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")  # .decode()는 byte데이터를 파이썬 유니코드 문자열로 변화한다
        self.assertEqual(response.content.decode(), expected_html)  # 즉 문자열과 문자열을 비교를 하는 것이다







