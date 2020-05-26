# [chapter03] 단위 테스트를 이용한 간단한 홈페이지 테스트

### 단위테스트 vs 기능테스트

단위테스트는 프로그래머 관점에서 그 내부를 테스트 하는 것이고 기능테스트는 사용자 관점에서 애플리케이션 외부를 테스트하는 것입니다.

양쪽 테스트를 다 알아볼 것이며 작업순서는 다음과 같습니다.

1. 기능 테스트를 작성해서 사용자 관점에서 새로운 기능 정의
2. 기능테스트를 실패하면 어떻게 코드를 작성해야 성공할지 생각 후, 이 시점에서 단위테스트를 이용해 코드가 어떻게 동작해야 하는지 정의
3. 단위 테스트가 실패하면 단위 테스트를 통과할 수 있을 정도의 최소 코드 작성
4. 테스트가 완전해질 때까지 2,3 반복하며 테스트 확인

과정을 보며 기능테스트는 상위 레벨의 개발을, 단위테스트는 하위 레벨을 주도하는 것을 확인할 수 있습니다.



### Django에서의 단위 테스트

단위 테스트를 진행하기 위해서 우선 app을 만들도록 하겠습니다.

``` shell
python manage.py startapp lists
```



django에서 테스트는 app 내의 `tests.py` 에서 이루어집니다.

기존 `unittest.TestCase` 의 확장버전을 사용합니다.

고의적인 실패테스트를 만들어봅시다.

``` python
# lists/tests.py

from django.test import TestCase


class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1+1, 3)
```



이를 실행하는 방법은 다음과 같습니다.

``` shell
python manage.py test
```



예상대로 결과는 실패입니다.

```shell
Traceback (most recent call last):
  File "/Users/rkdalstjd9/Desktop/prography/python-test-driven-development/project/lists/tests.py", line 6, in test_bad_maths
    self.assertEqual(1+1, 3)
AssertionError: 2 != 3

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
Destroying test database for alias 'default'...
```



이를 통해 우리가 처리해야할 테스트는 아래 두 가지입니다.

* URL의 사이트 루트("/")를 해석해서 특정 뷰 기능에 매칭 시킬 수 있는가?
* 이 뷰 기능이 특정 HTML을 반환하게 해서 기능 테스트를 통과할 수 있는가?



첫 번째 테스트를 위해서 기본적인 코드들을 작성하겠습니다.

``` python
# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lists.urls')),
]
```

```python
# lists.urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
]
```

```python
# lists.views.py

from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return HttpResponse("<html><title>To-Do lists</title></html>")
```



이제 test를 작성해보겠습니다.

``` python
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        # resolve를 통해 URL에 해당하는 view를 찾고 이를 실행
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
```



