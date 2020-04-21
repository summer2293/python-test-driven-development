# [chapter04] 왜 테스트를 하는 것인가?

`chapter3`를 보면 views, urls, tests 등의 코드를 한 번에 작성한 것을 확인할 수 있습니다. 하지만 이는 실제로 별로 좋은 방법이 아닙니다.

완벽하고 철저한 TDD를 위해서는 간단한 함수나 상수를 위해서도 테스트가 이루어져야 합니다. 물론 이러한 과정이 하찮게 여겨질 수도 있지만 그렇다고 해서 이 과정들을 건너뛴다면, 이후에 개발자가 알지 못하는 사이에 어플리케이션의 복잡성이 커지게 되는 위험이 있습니다.



### 셀레늄을 이용한 사용자 반응 테스트

`functional_tests.py` 를 다음과 같이 수정하겠습니다.

``` python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome("./chromedriver")
        self.browser.implicitly_wait(3)

    def testDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 사이트 접속
        self.browser.get('http://localhost:8000')
        # title 확인
        self.assertIn('To-Do', self.browser.title)
        # header 확인
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 작업추가
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        # 텍스트 입력
        inputbox.send_keys('공작깃털 사기')

        # 엔터키 입력 시 페이지가 갱신되고 작업목록에 입력한 데이터 추가
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = tables.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: 공작깃털 사기' for row in rows),
            "신규 작업이 테이블에 표시되지 않는다."
        )

if __name__ == '__main__':
    unittest.main(warnings='ignore')
```

> find_elment_by, find_elements_by 
>
> 두 함수는 s의 차이가 있습니다. 전자는 하나의 요소만 반환하며 없는 경우 예외를 발생시키고, 후자는 리스트를 반환하며 없는 경우 빈 리스트를 반환합니다.
>
> 이 함수들은 generator expression 으로 list comprehension보다 더 진보된 기술입니다.

결과는 다음과 같습니다.

실패지만 아직 \<h1> 요소가 없으므로 당연한 결과이죠.

``` shell
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"h1"}
```



### 상수는 테스트하지마라

다시 돌아와서 `lists/tests.py` 의 코드를 보면 특정 html 문자열을 확인하고 있습니다. 하지만 이것은 효율적인 방법이 아닙니다.

단위 테스트 시에 일반적인 규칙 중 하나는 **상수는 테스트하지마라** 이며 html을 문자열로 테스트하는 것은 상수 테스트와 다를 바 없습니다.

우선 기존의 코드를 리텍토링합시다.

```python
# settings.py

INSTALLED_APPS = [
		# 생략
    'lists',
]
```

``` html
<!-- lists/templates/lists/home.html -->

<html>
    <title>To-Do lists</title>
</html>
```

``` python
from django.shortcuts import render

def home_page(request):
    return render(request, 'lists/home.html')
```



이게 상수를 테스트하는 것이 아닌 구현 결과물을 비교하도록 하겠습니다.

`render_to_string` 를 통해 html파일을 string으로 바꿔주고, `decode` 를 통해 마찬가지로 `response.content` 를 바이트에서 string으로 바꿔주었습니다.

``` python
# lists/tests.py

def test_home_page_returns_correct_html(self):
    request = HttpRequest()
    response = home_page(request)
    expected_html = render_to_string('lists/home.html')
    self.assertEqual(response.content.decode(), 
expected_html)
```



### 메인 페이지 추가 수정

다시 기능 테스트로 돌아옵시다.

기능 테스트를 성공적으로 수행하기 위해서 `home.html` 을 수정하겠습니다.

``` html
<!-- templates/lists/home.html -->

<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
        <input id="id_new_item" placeholder="작업 아이템 입력" />
        <table id="id_list_table">
        </table>
    </body>
</html>
```



이제 FT를 실행하면 다음과 같은 에러를 확인할 수 있습니다. 

이는 다음 chapter에서 이어서 해결 해보도록 하겠습니다.

``` shell
AssertionError: False is not true : 신규 작업이 테이블에 표시되지 않는다.

----------------------------------------------------------------------
Ran 2 tests in 8.593s

FAILED (failures=1)
```



###  TDD 프로세스

![TDD process from Test Driven Development](https://img1.daumcdn.net/thumb/R720x0.q80/?scode=mtistory&fname=http%3A%2F%2Fcfile6.uf.tistory.com%2Fimage%2F99806533598BE30627E698)

TDD 프로세스 중에 가장 어려운 점은 `Write minimal code` 인 듯 합니다.

