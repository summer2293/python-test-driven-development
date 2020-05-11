from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from unittest import skip


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        # executed once before the first test.
        super().setUpClass()
        cls.browser = webdriver.Chrome(ChromeDriverManager().install())

    @classmethod
    def tearDownClass(cls):
        # executed once after the last test.
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        # executed before each test.
        super(FunctionalTest, self).setUp()

    def tearDown(self) -> None:
        # executed after each test.
        super(FunctionalTest, self).tearDown()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
