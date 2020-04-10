from django.urls import reverse, resolve
from django.test import TestCase
from .views import home_page

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self): 
        found = resolve('/') # 책과 다르게 reverse. 변경되었다.
        self.assertEqual(found.func, home_page) # homepage 와 맞는지 check