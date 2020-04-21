from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    # setUp과 testDown은 테스트 시작 전후에 실행
    def setUp(self):
        self.browser = webdriver.Chrome("./chromedriver")
        self.browser.implicitly_wait(3)

    # 테스트에서 에러가 발생해도 testDown이 실행
    # setUp에서 발생하는 것은 실행 X 
    def testDown(self):
        self.browser.quit()

    # test라는 명칭으로 시작하는 모든 메소드는 테스트 메소드
    # 클래스 당 하나 이상의 테스트 메소드 가능
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

if __name__ == '__main__':
    # unittest.main을 호출해서 unittest 테스트 실행자를 가동
    # warnings='ignore'는 테스트 작성 시 발생하는 불필요한 리소스 경고를 제거
    unittest.main(warnings='ignore')