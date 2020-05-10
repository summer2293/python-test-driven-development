from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 톰이 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고
        # 웹 사이트를 확인하러 간다
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀이 'To-Do'를 표시하고 있다
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # 바로 작업을 추가한다.
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "작업 아이템 입력")

        # 텍스트를 입력한다.
        inputbox.send_keys("공작깃털 사기")

        # 엔터키를 누르면 새로운 URL로 바뀐다. 그리고 작업 목록에 추가된다.
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")
        self.check_for_row_in_list_table("1: 공작깃털 사기")

        # 추가 아이템을 입력할 수 있는 텍스트 상자가 아직 존재한다.
        # 텍스트 입력
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("공작깃털을 이용해서 그물 만들기")
        # 엔터키 입력 시 페이지가 갱신되고 작업목록에 입력한 데이터 추가
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table("1: 공작깃털 사기")
        self.check_for_row_in_list_table("2: 공작깃털을 이용해서 그물 만들기")

        # 새로운 사용자인 프란시스가 사이트에 접속한다.

        # 새로운 브라우저 세션을 이용해서 에디스의 정보가 쿠키를 통해 유입되는 것을 방지한다.
        self.browser.quit()
        self.browser = webdriver.Chrome("./chromedriver")

        # 프란시스가 홈페이지에 접속한다
        # 에디스의 리스트는 보이지 않는다
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("공작깃털 사기", page_text)
        self.assertNotIn("그물 만들기", page_text)

        # 프란시스가 새로운 작업 아이템을 입력하기 시작한다
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("우유 사기")
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL을 취득한다.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없다는 것을 다시 확인한다.
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("공작깃털 사기", page_text)
        self.assertIn("우유 사기", page_text)

        # 강제로 테스트 실패를 발생시킨다.
        self.fail("Finish the test!")
