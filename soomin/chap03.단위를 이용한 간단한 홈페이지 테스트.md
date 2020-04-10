## chap03.단위를 이용한 간단한 홈페이지 테스트

#### 첫 Django 애플리케이션과 첫 단위 테스트

app 만들기

```python
$ python3 manage.py startapp
```



#### 단위 테스트는 무엇이고，기능 테스트와 어떤 차이가 있을까?

##### 기능테스트

사용자 관점에서 애플리케이션 __외부__ 를 테스트한다. 제대로 된 기능성을 갖춘 애플리케이션을 만들어준다.

##### 단위테스트

프로그래머 관점에서 내부를 테스트한다. 단위 테스트는 버그없는 코드를 작성하도록 도와준다.

##### FLOW

1. 사용자 관점의 새로운 기능을 정의한다. (기능 테스트)
2. 기능테스트를 실패하면 어떻게 코드를 작성해야 성공할지 생각한다. 이 시점에서 단위테스트를 통해 기능을 정의한다.
3. 단위 테스트가 실패하면 통과할 만한 최소 코드 작성 
4. 통과 확인



#### Django 에서 단위 테스트

lists/test.py

> django 에서는 unittest.TestCase 의 확장버전인 django.test 를 제공해준다.

```python
from django.test import TestCase

# Create your tests here.

```



##### 고의적인 실패테스트만들어보기

```python
from django.test import TestCase

class SmokeTest(TestCase):
    def test_bad_maths(self): 
    	self.assertEqual(l + l, 3)
```

```python
$ python3 manage.py test
```

```
ERROR: test_bad_maths (lists.tests.SmokeTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/Soomti/Desktop/odk/python-tdd/soomin/tddjango/superlists/lists/tests.py", line 6, in test_bad_maths
    self.assertEqual(l + l, 3)
NameError: name 'l' is not defined

----------------------------------------------------------------------
Ran 1 test in 0.001s

```





#### Django의 MVC, URL, 뷰 함수

django 는 MTV 패턴을 사용한다

> 1. 특정 URL에 대한 HTTP “요청”을 받는다.
> 2.  Django는 URL 을 작성하여, 해당 URL 이 들어오면  어떤 뷰 함수를 실행할지 결정한다. (URL “해석”이라고 하는 처리다). 
> 3. 이 뷰 기능이 요청을 처리해서 HTTP “응답”으로 반환한다. 



##### 테스트 할 것

1. URL이 루트를 해석해서 뷰에 매칭을 시킬 수 있을까?
2. 뷰 기능이 특정 HTML을 반환하게 해서 기능 테스트틀 통과할 수 있는가?

```python
from django.urls import reverse
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self): 
        found = reverse('/') # 책과 다르게 reverse. 변경되었다.
        self.assertEqual(found.func, home_page) # homepage 와 맞는지 check
```

##### reverse()

해당 url에 대한 도메인 외 url 을 리턴해준다.

https://wayhome25.github.io/django/2017/05/05/django-url-reverse/





views.py

```python
from django.shortcuts import render

home_page = None
```

