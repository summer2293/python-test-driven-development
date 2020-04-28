# 1. LiveServerTestCase 추가
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        # 4. ChromeDriver 변경
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3)

    def tearDown(self):
        time.sleep(3)
        self.browser.quit()

    def check_for_row_int_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 2. 로컬 호스트 접속 하드코딩 수정
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        inputbox.send_keys('공잣깃털 사기')
        inputbox.send_keys(Keys.ENTER)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공잣깃털을 이용하여 그물 만들기')
        inputbox.send_keys(Keys.ENTER)
        
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_int_list_table("1: 공잣깃털 사기")
        self.check_for_row_int_list_table("2: 공잣깃털을 이용하여 그물 만들기")

        # 새로운 브라우저 세션을 이용해서 에디스의 정보가 쿠키를 통해 유입되는 것을 방지
        self.browser.quit()
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        # 프란시스가 홈페이지에 접속
        # 에디스의 리스트가 보이지 않는다.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        # 프란시스가 새로운 작업 아이템을 입력하기 시작
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL을 취득
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없다는 것을 다시 확인
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)






# 3. if __name__ == '__main__': 삭제