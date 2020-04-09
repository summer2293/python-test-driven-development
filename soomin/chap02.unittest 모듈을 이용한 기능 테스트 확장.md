## chap02.unittest 모듈을 이용한 기능 테스트 확장

#### 기능 테스트란

>  기능 동작 방식 테스트. 특정 기능을 사용자가 어떻게 하는지 상황극(?) 을 통해 테스트한다

sample 

```python
from selenium import webdriver

browser = webdriver.Chrome("./chromedriver")

# 에디스(Edith)는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고 
# 해당 웹 사이트를 확인하러 간다
browser.get('http://localhost:8000')

# 웹 페이지 타이틀과 헤더가 'To-Do' 를 표시하고 있다.
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

> #### 주석에 대해서...
>
> ```python
> # wibble 값을 1 늘린다 
> wibble += 1
> ```
>
> 코드 자체만 보고도 해석 가능한 주석은 지양하자.



python 에서 assertion error에 대해 명확한 값을 알고싶은 경우, try / execept 를 이용 할 수 있지만, 테스트 시 자주 발생하기 때문에 python에서는 unittest 모듈을 제공해준다.

#### python unittest 모듈

```python
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome("./chromedriver")
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        # 에디스(Edith)는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고 
        # 해당 웹 사이트를 확인하러 간다
        self.browser.get('http://localhost:8000')
        # 웹 페이지 타이틀과 헤더가 'To-Do' 를 표시하고 있다.
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
     unittest.main(warnings='ignore') 

```

##### setUp

시작 전에 시작하는 모듈

##### tearDown

끝날 때 시작하는 모듈

##### assertIn

유닛테스트에서 제공하는 테스트 메서드.

https://docs.python.org/ko/3/library/unittest.html

> Junit 단위테스트랑 비슷하다.
>
> ##### test fixture
>
> 테스트 수행 전 준비 작업
>
> ##### test case
>
> 테스트의 개별 단위
>
> ##### Test 묶음
>
> 여러 테스트 케이스 
>
> ##### assert method a 종류
>
> ```python
> assertEqual(a, b) # a == b
> 
> assertNotEqual(a, b) # a != b
> 
> assertTrue(x) # bool(x) is True
> 
> assertFalse(x) # bool(x) is False
> 
> assertIs(a, b) #a is b
> 
> assertIsNot(a, b) # a is not b
> 
> assertIsNone(x) # x is None
> 
> assertIsNotNone(x) # x is not None
> 
> assertIn(a, b) # a in b
> 
> assertNotIn(a, b)# a not in b
> 
> assertIsInstance(a, b) # isinstance(a, b)
> 
> assertNotIsInstance(a, b) # not isinstance(a, b)
> ```

- fail()

  강제적으로 테스트 실패를 발생시켜 에러메세지를 출력. 테스트가 끝남을 알려준다.

###### 실행 후 

```python
$ python3 functional_test.py
```

```python

FAIL: test_can_start_a_list_and_retrive_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_test.py", line 17, in test_can_start_a_list_and_retrive_it_later
    self.assertIn('To-Do', self.browser.title)
AssertionError: 'To-Do' not found in 'localhost'

----------------------------------------------------------------------
Ran 1 test in 3.158s

FAILED (failures=1)
```



#### 암묵적 대기 

셀레늄을 시작할 때 대기시간 3초를 걸어준다.

```python
def setup(self):
	self.browser = webdriver.Firefox() 
    self.browser.implicitly_wait(3) # 3초
```

##### implicitly_wait

필요에 따라 지정한 시간(초 단위)만큼 동작을 대기 상태로 둘 수 있다. 

