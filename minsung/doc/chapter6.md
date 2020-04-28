# [chapter06] 최소 동작 사이트 구축

현재까지의 기능테스트는 문제점이 있습니다.

테스트를 할 때마다 테스트에서 사용된 작업 아이템이 데이터베이스에 남는 다는 것이죠.

이번 장에서는 이러한 문제점들을 해결하도록 하겠습니다.





### 기능 테스트 내에서 테스트 격리

단위 테스트의 경우, Django 테스트 실행자가 자동으로 새로운 테스트 데이터베이스를 생성하기 때문에 다음과 같은 문제가 발생하지 않습니다. 

하지만 기능테스트는 현재 실제 데이터베이스인 `db.sqlite3` 를 사용하고 있기 때문에 이러한 문제가 발생하죠.



이를 위해서 `LiveServerTestCase` 를 사용하도록 하겠습니다.

이는 단위 테스트와 마찬가지로 테스트용 데이터베이스를 생성해줍니다.

이를 사용하기 위해서 디렉토리 구조를 변경해주었습니다.

`lists` 앱과 같은 경로에 functional_tests 를 생성하고 그 안에 `__init.py` 와 `tests.py` 를 추가해줍니다.

`__init__.py` 를 추가함으로 인해서 django 에서 해당 폴더를 알릴 수 있고 이제 python manage.py 를 통해 기능테스트를 할 수 있습니다.

``` 
.
├── config
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── functional_tests
│   ├── __init__.py
│   ├── chromedriver
│   └── tests.py
├── lists
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── templates
│   │   └── lists
│   │       └── home.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── requirements.txt
```



이제 `LiveServerTestCase`를 사용ㅎ기 위해 tests.py 를 수정하도록 합시다.

1. LiveServerTestCase 추가

2. 로컬 호스트 접속 하드코딩 수정

3. `if __name__ == '__main__':` 삭제

4. ChromeDriver 변경

   `ChromeDriver`를 사용하기 위해서 `webdriver_manager` 를 설치해주었습니다.

   ``` bash
   pip install webdriver-manager
   ```

   자동으로 OS와 브라우저 버젼에 맞는 `webdriver` 를 설치해줍니다.

   한 번 설치한 이유에는 캐싱하여 사용합니다.

   ``` 
   Looking for [chromedriver 81.0.4044.69 mac64] driver in cache 
   ```

   

``` python
# project/functional_tests/tests.py

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

        # 텍스트 입력
        inputbox.send_keys('공작깃털 사기')

        # 엔터키 입력 시 페이지가 갱신되고 작업목록에 입력한 데이터 추가
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_int_list_table("1: 공잣깃털 사기")
        self.check_for_row_int_list_table("2: 공잣깃털을 이용하여 그물 만들기")


# 3. if __name__ == '__main__': 삭제
```



물론 아직까지 테스트는 실패합니다.



> 이제 기능테스트도 manage.py를 통해 실행함으로서 기능테스트와 단위테스트의 실행이 헷갈릴 수 있습니다.
>
> 기능테스트 및 단위 테스트 실행
>
> ``` 
> python manage.py test
> ```
>
> 기능테스트 실행
>
> ``` 
> python manage.py test {기능테스트가 코드가 있는 폴더 이름}
> ```
>
> 단위 테스트 실행
>
> ```
> python manage.py test {엡이름}
> ```
>
> 







### TDD를 이용한 새로운 설계 반영하기

에디스가 첫번째 아이템을 전송하자마자 새로운 목록을 만들어서 신규 작업 아이템을 추가한다.

그리고 그녀가 만든 목록에 접근할 수 있는 URL을 제공한다. 

> 저번 코드에 `공잣깃털을 이용하여 그물 만들기` 를 추가하는 코드를 생략한 듯 하여 17번째 줄에 추가하였습니다.

```python
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
    
    inputbox.send_keys('공작깃털 사기')
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
```



테스트를 실행시키면 예상한 실패를 얻을 수 있습니다.

``` 
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rkdalstjd9/Desktop/prography/python-test-driven-development/minsung/project/functional_tests/tests.py", line 39, in test_can_start_a_list_and_retrieve_it_later
    self.assertRegex(edith_list_url, '/lists/.+')
AssertionError: Regex didn't match: '/lists/.+' not found in 'http://localhost:54461/'

----------------------------------------------------------------------
Ran 1 test in 7.208s
```





### 새로운 설계를 위한 반복

다음으로는 Regexp 불일치 문제를 가지고 있는 FT가 두 번째 아이템에 개별 URL과 식별자를 적용하는 것이 다음 작업입니다.

다음과 같이 수정해줍니다.

``` python
# lists/tests.py

def test_home_page_redirects_after_post(self):
    # 생략
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


# lists/views.py

def home_page(request):
    # 생략
    return redirect('/lists/the-only-list-in-the-world/')
```





### Django 테스트 클라이언트를 이용한 뷰, 템플릿, URL 동시 테스트

여태까지는 URL 해석, 뷰 함수 호출, 템플릿 렌더링에 대해서 하나씩 해주었지만 Django에서는 이를 한 번에 처리할 수 있도록 지원해줍니다.

새로운 테스트 클래스를 선언해주도록 합시다.

``` python
# lists/tests.py

class LiveViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
```



결과는 예상대로 실패입니다.

``` 
FAIL: test_displays_all_items (lists.tests.LiveViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rkdalstjd9/Desktop/prography/python-test-driven-development/minsung/project/lists/tests.py", line 87, in test_displays_all_items
    self.assertContains(response, 'item1')
  File "/usr/local/lib/python3.7/site-packages/django/test/testcases.py", line 446, in assertContains
    response, text, status_code, msg_prefix, html)
  File "/usr/local/lib/python3.7/site-packages/django/test/testcases.py", line 418, in _assert_contains
    " (expected %d)" % (response.status_code, status_code)
AssertionError: 404 != 200 : Couldn't retrieve content: Response code was 404 (expected 200)

----------------------------------------------------------------------
```



아까부터 사용하고 있던 `/lists/the-only-list-in-the-world/` 이 제대로 동작하도록 추가해주겠습니다.

``` python
# lists/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('lists/the-only-list-in-world/', views.view_list),
]


# lists/views.py


def view_list(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'lists/home.html', context)
```



현재까지 단위 테스트는 전부 통과, 기능 테스트는 아래와 같이 예상된 실패입니다.

``` 
AssertionError: '2: 공잣깃털을 이용하여 그물 만들기' not found in ['1: 공잣깃털 사기']
```



> 리펙토링하고 넘어갑시다.
>
> lists/tests.py 에서 `test_displays_all_items` 를 추가함으로서 기존에 있던 `test_home_page_displays_all_list_items` 은 불필요해졌습니다.
>
> 삭제하겠습니다,.



#### 목록 출력을 위한 별도 템플릿

메인페이지와 목록 뷰 기능이 다르기 때문에 각각 별개의 html 탬플릿을 사용하는 것이 좋습니다.

home.html은 하나의 입력상자를 가지며, list.html은 기존 아이템을 보여주는 테이블을 가집니다.

서로 다른 템플릿을 확인하는 테스트를 추가해봅시다.

``` python
# lists/tests.py

class LiveViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')
        
    # 생략
```



해당 테스트를 통과하기 위해서 `home.html` , `list.html` 을 추가하고 views를 수정해봅시다.

`home.html` 은 table을 제거해주고, `list.html` 은 form action을 추가해주었습니다.

``` html
<!-- templates/lists/home.html -->

<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list in home</h1>
        <form method="POST" action="">
            <input name="item_text" id="id_new_item" placeholder="작업 아이템 입력" />    
            {% csrf_token %}
        </form>
    </body>
</html>

<!-- templates/lists/list.html -->

<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
        <form method="POST" action="/">
            <input name="item_text" id="id_new_item" placeholder="작업 아이템 입력" />    
            {% csrf_token %}
        </form>
        <table id="id_list_table">
            {% for item in items %}
                <tr><td>{{forloop.counter}}: {{ item.text }}</td></tr>
            {% endfor %}
        </table>
    </body>
</html>
```



`home_page` 는 데이터를 render해줄  필요가 없어서 삭제하였고 `view_list` 는 `list.html` 를 render해줍니다.

``` python
# lists/views.py

def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'lists/home.html')
  
def view_list(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'lists/list.html', context)
```



현재까지 단위테스트는 무사히 성공하고 기능테스트는 아래와 같이 예상된 결과를 출력합니다.

``` 
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rkdalstjd9/Desktop/prography/python-test-driven-development/minsung/project/functional_tests/tests.py", line 67, in test_can_start_a_list_and_retrieve_it_later
    self.assertNotEqual(francis_list_url, edith_list_url)
AssertionError: 'http://localhost:55547/lists/the-only-list-in-the-world/' == 'http://localhost:55547/lists/the-only-list-in-the-world/'

----------------------------------------------------------------------
Ran 1 test in 10.243s
```





### 목록 아이템 추가하기 위한 URL과 뷰



