from selenium import webdriver
import unittest


from selenium import webdriver # 

browser = webdriver.Chrome("./chromedriver") # 이걸 해야함..
browser.get('http://localhost:8000')

assert 'Django' in browser.title


# class NewVisitorTest(unittest.TestCase):
    
#     def setUp(self):
#         self.browser = webdriver.Chrome("./chromedriver")
    
#     def tearDown(self):
#         self.browser.quit()

#     def test_can_start_a_list_and_retrive_it_later(self):
#         # 에디스(Edith)는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고 
#         # 해당 웹 사이트를 확인하러 간다
#         self.browser.get('http://localhost:8000')
#         # 웹 페이지 타이틀과 헤더가 'To-Do' 를 표시하고 있다.
#         self.assertIn('To-Do', self.browser.title)
#         self.fail('Finish the test!')


# if __name__ == '__main__':
#      unittest.main(warnings='ignore') 




# # 그녀는 바로 작업을 추가하기로 한다
# # 공작깃털 사기 라고 텍스트 상자에 입력한다
# # (에디스의 취미는 날치 잡이용 그물을 만드는 것이다)
# # 엔터키를치면  이지가 갱신되고작업 목록에 #  1: 공작깃털 사기  아이템이 추가된다
# # 추가아이템을입력할수있는여분의텍스트상자가존재한다
# # 다시  공작깃털을 이용해서 그물 만들기 라고 입력한다 (에디스는 매우 체계적인 사람이다)
# # 이지는다시 갱신되고, 두 개 아이템이 목록에보인다
# # 에디스는 사이트가 입력한 목록을 저장하고 있는지 궁금하다 # 사이트는 그녀를 위한 특정 URL을 생성해준다
# # 이때URL에대한설명도함께제공된다
# # 해당URL에접속하면그녀가만든작업목록이그대로있는것을확인할수있다 # 만족하고잠자리에든다
# browser.quit()



