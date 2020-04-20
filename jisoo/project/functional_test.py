from selenium import webdriver
import unittest

# browser = webdriver.Chrome('./chromedriver')

# # 톰이 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고
# # 웹 사이트를 확인하러 간다
# browser.get('http://localhost:8000')

# # 웹 페이지 타이틀이 `To-Do`를 표시하고 있다
# assert 'To-Do' in browser.title, "Browser title was " + browser.title 

# browser.quit()

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 톰이 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고
        # 웹 사이트를 확인하러 간다
        self.browser.get('http://localhost:8000')

        # 웹 페이지 타이틀이 'To-Do'를 표시하고 있다
        self.assertIn('To-Do', self.browser.title)
        # 강제로 테스트 실패를 발생시킨다.
        self.fail('Finish the test!')
    
if __name__ == '__main__':
    unittest.main()