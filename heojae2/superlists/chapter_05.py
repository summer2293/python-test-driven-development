from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from webdriver_manager.chrome import ChromeDriverManager
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # self.browser = webdriver.Firefox(executable_path=r'/home/shrldh3576/바탕화면/Gekodriver/geckodriver')
        # 파이어 폭스로 실행을 할때에는 되지 않지만,  구글 크롬 드라이버로 실행을 하니 또 되는 군요 되게 신기하네!
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        # 에디스(Edith)는  멋진 작업 목록 온라인  앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다
        self.browser.get('http://127.0.0.1:8000/')

        # 웹 페이지  타이틀과 헤더가 "To - Do"를 표시하고 있다.
        header_text = self.browser.find_element_by_tag_name('h1').text
        print("header_text",header_text)
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "작업 아이템 입력"
        )

        # "공작깃털 사기"라고 텍스트 상자에 입력을 한다
        # (에디스의 취미는 날치 잡이용 그물을 만드는 것이다 )
        inputbox.send_keys("공작 깃털 사기")

        # 엔터키를 치면 페이지가 갱신이 되고, 작업 목록에
        # "1: 공작 깃털 사기" 아이템이 추가된다
        inputbox.send_keys(Keys.ENTER)
        time.sleep(10)

        self.check_for_row_in_list_table("1: 공작 깃털 사기")

        # 추가 아이켐을 입력할 수 있는 여분의 텍스트 상자가 존재한다
        # 다시 "공작 깃털을 이용해서 그물을 만들기"라고 입력한다 (에디스는 매우 체계적인 사람이다 )
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("공작 깃털을 이용해서 그물을 만들기")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 페이지가 갱신이 되고, 두개의 아이템이 목록에 보인다
        self.check_for_row_in_list_table('2: 공작 깃털을 이용해서 그물을 만들기')
        self.check_for_row_in_list_table("1: 공작 깃털 사기")

        # 에디스는 사이트가 입력한 목록을 저장하고 있는지 궁금하다

        # 사이트는 그녀를 위한 특정한 URL을 생성을 해준다
        # 이때 URL에 대한 설명도 함께 제공된다
        self.fail('Finish the test!')

        # 해당 URL에 접속을 하면 그녀가 만든 작업 목록이 그대로 있는 것을 확인 할 수 있다
        # 만족하고 잠자리에 든다



if __name__ == '__main__':
    unittest.main(warnings='ignore')