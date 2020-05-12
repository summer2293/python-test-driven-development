# 1. LiveServerTestCase 추가
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time


class FunctionalTest(StaticLiveServerTestCase):
    # @classmethod
    # def setUpClass(cls):
    #     pass
    # @classmethod
    # def testDownClass(cls):
    #     pass

    def setUp(self):
        # 4. ChromeDriver 변경
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3)

    def tearDown(self):
        time.sleep(3)
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
