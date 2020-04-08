from django.urls import reverse
from django.test import TestCase
from lists.views import home_page
# Create your tests here.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self): 
        found = reverse('/') # 책과 다르게 reverse. 변경되었다.
        self.assertEqual(found.func, home_page) # homepage 와 맞는지 check

