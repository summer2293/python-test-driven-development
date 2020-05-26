# [chapter02] unittest 모듈을 이용한 기능 테스트 확장

### 기능 테스트를 이용한 최소 기능의 애플리케이션 설계

#### 기능테스트

기능테스트란 사용자 관점에서 애플리케이션이 어떻게 동작 하는지 확인할 수 있는 테스트를 말합니다. 승인테스트, 종단간 테스트, 블랙박스 테스트 등 다양한 용어로 불리기도 합니다. 해당 글에서는 기능테스트, functional test를 줄여서 FT라고 부르도록 하겠습니다.



FT는 사람이 이해할 수 있는 스토리를 가지고 있어야 합니다. 다음과 같이 테스트 코드보다 주석이 선행 될 수도 있습니다.

```python
from selenium import webdriver

browser = webdriver.Chrome("./chromedriver")

# 웹사이트 접속
browser.get('http://localhost:8000')

# 웹사이트 타이틀과 헤더가 To-Do를 표시하는지 확인
assert 'To-Do' in browser.title

# 그녀는 바로 작업을 추가하기로 한다
# 공작깃털 사기 라고 텍스트 상자에 입력한다
# (에디스의 취미는 날치 잡이용 그물을 만드는 것이다)
# 엔터키를치면  이지가 갱신되고작업 목록에 #  1: 공작깃털 사기  아이템이 추가된다
# 추가아이템을입력할수있는여분의텍스트상자가존재한다
# 다시  공작깃털을 이용해서 그물 만들기 라고 입력한다 (에디스는 매우 체계적인 사람이다)
# 이지는다시 갱신되고, 두 개 아이템이 목록에보인다
# 에디스는 사이트가 입력한 목록을 저장하고 있는지 궁금하다 # 사이트는 그녀를 위한 특정 URL을 생성해준다
# 이때URL에대한설명도함께제공된다
# 해당URL에접속하면그녀가만든작업목록이그대로있는것을확인할수있다 # 만족하고잠자리에든다
browser.quit()
```



### 파이썬 기본 라이브러리의 unittest 모듈

`assert`에서 다음과 같이 현재의 browser title을 확인할 수 있습니다.

``` python
assert 'To-Do' in browser.title, "Browser title was " + browser.title
```

```shell
Traceback (most recent call last):
  File "functional_test.py", line 9, in <module>
    assert 'To-Do' in browser.title, "Browser title was " + browser.title
AssertionError: Browser title was Django: the Web framework for perfectionists with deadlines.
```



에러 핸들링을 위해서 `try/except` 문을 사용할 수 도 있지만 이런 문제는 테스트 시에 자주 발생하는 이슈이기 때문에 `unittest` 라는 별도의 솔루션이 존재합니다.

``` python
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    # setUp과 testDown은 테스트 시작 전후에 실행
    def setUp(self):
        self.browser = webdriver.Chrome("./chromedriver")

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
```



다음과 같은 실행 결과를 확인할 수 있습니다.

`assertIn` 가 몇 개의 테스트가 실행되었고 그 중 몇 개가 실패했는지 보여줍니다.

```shell
Traceback (most recent call last):
  File "functional_test.py", line 14, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('To-Do', self.browser.title)
AssertionError: 'To-Do' not found in 'Django: the Web framework for perfectionists with deadlines.'

----------------------------------------------------------------------
Ran 2 tests in 4.987s

FAILED (failures=1)
```



unittest`에 대해서는 아래 링크에서 자세하게 살펴볼 수 있습니다.

https://docs.python.org/ko/3/library/unittest.html



### 왜 test가 두 개 도는 걸까?

위 결과를 살펴보면 테스트가 두 개가 돌아간 것을 확인할 수 있습니다.

``` shell
Ran 2 tests in 4.987s
```

책이나 다른 분들의 결과에서는 test가 1개 였기 때문에 무엇이 문제인지 찾다가 오타로 인한 것을 알 수 있었습니다.

`tearDown` 을 `testDown` 으로 잘못 기재 했기 때문에 `testDown` 을 테스트 후에 발생시키는 함수가 아닌 test함수 처럼 인식하여 실행시킨 것이죠.

그리고 위에 코드는 현재 브라우저를 열고, 닫고 2회 반복하게 됩니다.

python 공식문서에 따르면 

> [`setUp()`](https://docs.python.org/ko/3/library/unittest.html#unittest.TestCase.setUp)과 [`tearDown()`](https://docs.python.org/ko/3/library/unittest.html#unittest.TestCase.tearDown) 메서드로 각각의 테스트 메서드 전과 후에 실행될 명령어를 정의할 수 있습니다.

`setUp`과` tearDown`은 각각의 test 메서드 앞 뒤로 실행되는 것이기 때문에 2회 반복되는 것이 맞았습니다.

시험을 위해 test 메서드를 n개 작성할 경우,  두 메서드도 n번 호출 되는 것을 확인할 수 있습니다.



### 암묵적 대기

셀레늄은 비교적 안정적으로 페이지 로딩이 끝날 때까지 기다렸다가 테스트를 실행하지만 완벽하지는 않습니다. 

따라서 `암묵적 대기`를 통해 지정한 시간만큼 동작을 대기 상태로 둡니다.

```python
def setUp(self):
    self.browser = webdriver.Chrome("./chromedriver")
    self.browser.implicitly_wait(3)
```

> 애플리케이션 구조가 간단한 경우에는 동작하지만 복잡한 경우에는 명시적인 대기 알고리즘을 작성해야 한다.

