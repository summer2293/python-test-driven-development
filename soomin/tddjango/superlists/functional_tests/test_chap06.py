from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# import unittest


class NewVisitorTest(LiveServerTestCase):

    # 시작 전과 시작 후에 자동으로 실행하는 메서드.
    def setUp(self):
        self.browser = webdriver.Chrome("./chromedriver")
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrive_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "작업 아이템 입력")

        inputbox.send_keys("공작깃털 사기")
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")
        self.check_for_row_in_list_table("1: 공작깃털 사기")

        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("공작깃털을 이용해서 그물 만들기")
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table("2: 공작깃털을 이용해서 그물 만들기")
        self.check_for_row_in_list_table("1: 공작깃털 사기")

        # 새로운 사용자인 프란시스가 사이트에 접속한다

        # 새로운 브라우저 세션을 이용해 에디스의 정보가
        # 쿠키를 통해 유입되는 것을 방지한다
        self.browser.quit()
        self.browser = webdriver.Chrome("./chromedriver")

        # 프란시스가 홈페이지에 접속한다.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertIn("공작깃털 사기", page_text)
        self.assertIn("그물 만들기", page_text)

        # 프란시스가 새로운 작업 아이템을 입력하기 시작한다
        # 그는 에디스보다 재미가 없다
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("우유 사기")
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL 을 취득한다.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없다는 것을 다시 확인한다.
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertIn("공작깃털 사기", page_text)
        self.assertIn("우유 사기", page_text)

        # 둘 다 만족하고잠자리에든다

        # # # # 에디스는 사이트가 입력한 목록을 저장하고 있는지 궁금하다
        # # # # 사이트는 그녀를 위한 특정 URL을 생성해준다
        # # # # 이때 URL에 대한 설명도 함께 제공된다
        # self.fail("Finish the Test!")

        # # # # 해당 URL에 접속하면 그녀가 만든 작업 목록이 그대로 있는 것을 확인할 수 있다

        # # # #
