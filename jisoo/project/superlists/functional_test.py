from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 톰이 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고
        # 웹 사이트를 확인하러 간다
        self.browser.get('http://localhost:8000')

        # 웹 페이지 타이틀이 'To-Do'를 표시하고 있다
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 바로 작업을 추가한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

        # 텍스트를 입력한다.
        inputbox.send_keys('공작깃털 사기')

        # 엔터키를 치면 페이지가 갱신되고 작업 목록에 아이템이 추가된다
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')

        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 강제로 테스트 실패를 발생시킨다.
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
