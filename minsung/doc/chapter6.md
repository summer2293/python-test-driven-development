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

`test_home_page_can_save_a_POST_request` 와 `test_home_page_redirects_after_post` 를 새로운 클래스로 이동하고 새롭게 이름을 지어줍니다.

또한 Django 클라이언트 테스트를 이용해 수정해줍시다.

``` python
# lists/tests.py

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )

        print(Item.objects.all())

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')

    
    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )

        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
```



#### 신규 목록 생성을 위한 URL과 View

신규 목록 생성을 위한 url과 view를 만들어봅시다.

`home_page` 에서 POST 요청이 들어왔을 경우의 로직을 따로 때내어 `new_list` 로 만들어줍니다.

``` python
# lists/urls.py
urlpatterns = [
    # 생략
    path('lists/new', views.new_list),
]

# lists/views.py

def home_page(request):
    return render(request, 'lists/home.html')
  
# 생략

def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')
```

> 데이터베이스에 액션을 가하는  URL인 경우에는 url 뒤에  / 를 생략합니다.



이제 html 파일의 form을 새로운 url로 연동합니다.

``` html
<!-- home.html, list.html -->

<form method="POST" action="/lists/new">
```



기능 테스트에 대해 예상된 실패가 발생합니다.

``` 
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rkdalstjd9/Desktop/prography/python-test-driven-development/minsung/project/functional_tests/tests.py", line 69, in test_can_start_a_list_and_retrieve_it_later
    self.assertNotEqual(francis_list_url, edith_list_url)
AssertionError: 'http://localhost:57314/lists/the-only-list-in-the-world/' == 'http://localhost:57314/lists/the-only-list-in-the-world/'

----------------------------------------------------------------------
Ran 1 test in 10.057s

FAILED (failures=1)
```





### 모델 조정하기



```python
# lists/tests.py

import .models import Item, List

def test_saving_and_retrieving_items(self):
    list_ = List()
    list_.save()
    
    first_item = Item()
    first_item.text = "첫 번째 아이템"
    first_item.list = list_
    first_item.save()
    
    second_item = Item()
    second_item.text = "두 번째 아이템"
    second_item.list = list_
    second_item.save()
    
    saved_list = List.objects.first()
    self.assertEqual(saved_list, list_)
    
    saved_items = Item.objects.all()
    self.assertEqual(saved_items.count(), 2)
    
    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, "첫 번째 아이템")
    self.assertEqual(first_saved_item.list, list_)
    self.assertEqual(second_saved_item.text, "두 번째 아이템")
    self.assertEqual(second_saved_item.list, list_)
```



이에 맞춰서 `List` 모델을 만들어줍니다. 

모델을 수정한 다음에는 자동으로 makemigrations 와 migrate를 해줍시다.

```python
# lists/models.py

from django.db import models


class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
```



단위 테스트를 하면 뷰 테스트에서 3개의 error가 발생합니다.

이를 해결하기 위해 수정을 해주겠습니다.

지금 하는 수정은 `Item`이 생길 때마다  새로운 `List`를 만들어서 그에 대응 시키는건데 이는 정상적인 해결 방법이 아닙니다. 

하지만 TDD를 할 때는 다음과 같이 조심스럽게 진행해야 합니다.

```python
# lists/tests.py

def test_displays_all_items(self):
    list_ = List.objects.create()
    Item.objects.create(text='item1', list=list_)
    Item.objects.create(text='item2', list=list_)
    
# lists/views.py

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
```



### 각 목록이 하나의 고유 URL을 가져야 한다

오래된 `test_uses_list_template`  을 수정하고 `test_displays_only_items_for_that_list`  을 추가해줍니다. 

``` python
# lists/tests.py

class LiveViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="item1", list=correct_list)
        Item.objects.create(text="item2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="other item1", list=other_list)
        Item.objects.create(text="other item2", list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'other item1')
        self.assertNotContains(response, 'other item2')
```



테스트 실행 시 , 예상한 대로 404와 관련된 2개의 에러가 발생합니다.



urls이 파라미터를 전달 받도록 수정해줍시다.

```python
# lists/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('lists/<int:list_id>/', views.view_list),
    path('lists/new', views.new_list),
]

# lists/views.py

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    context = {
        'items': items
    }
    return render(request, 'lists/list.html', context)
```



기존에 사용하던 `/lists/the-only-list-in-the-world/` 대신에 `lists/<int:list_id>/` 을 사용함으로서 수정사항이 생깁니다.

``` python
# lists/tests.py

def test_redirects_after_post(self):
    response = self.client.post(
        '/lists/new',
        data={'item_text': '신규 작업 아이템'}
    )
    new_list = List.objects.first()
    self.assertRedirects(response, '/lists/%d/' %(new_list.id, ))
    
def test_displays_all_items(self):
    list_ = List.objects.create()
    Item.objects.create(text='item1', list=list_)
    Item.objects.create(text='item2', list=list_)
    
    response = self.client.get('/lists/%d/' %(list_.id,))
    
    self.assertContains(response, 'item1')
    self.assertContains(response, 'item2')
    
    
# lists/views.py

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
```



이제 단위 테스트는 문제없이 통과됩니다.

기능 테스트는 어떨까요?

아직 에러가 발생합니다.

``` 
AssertionError: '1: 공잣깃털 사기' not found in ['1: 공잣깃털을 이용하여 그물 만들기']
```



### 기존 목록에 아이템을 추가하기 위한 또 다른 뷰

기존 목록에 신규아이템을 추가하기 위한 URL과 뷰가 필요합니다.

이를 위한 단위 테스트를 추가합시다.

``` python
# lists/tests.py

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item/' % (correct_list.id,),
            data = {'item_text': '기존 목록에 신규 아이템'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '기존 목록에 신규 아이템')
        self.assertEqual(new_item.list, correct_list)

    
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item/' % (correct_list.id,),
            data={ 'item_text': '기존 목록에 신규 아이템'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
```



해당 url이 없으므로 결과는 예상대로 실패입니다.

``` 
AssertionError: 404 != 302 : Response didn't redirect as expected: Response code was 404 (expected 302)
```



이에 해당하는 url 과 view를 만들어줍시다.

``` python
# lists/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('lists/<int:list_id>/', views.view_list),
    path('lists/<int:list_id>/add_item/', views.add_item),
    path('lists/new', views.new_list),
]

# lists/views.py

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
```



현재까지 모든 테스트가 통과합니다.



`list.html` 과 연결시켜줍시다.
```html
<!-- templates/lists/list.html -->

<form method="POST" action="/lists/{{ list.id }}/add_item">
```



이것이 동작하기 위해서는 뷰가 목록을 탬플릿에게 전달해야합니다.

이를 테스트하는 단위 테스트를 작성합시다.

```python
# lists/tests.py LiveViewTest

def test_passes_correct_list_to_template(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    response = self.client.get('/lists/%d/' % (correct_list.id,))
    self.assertEqual(response.context['list'], correct_list)
```

`response.context` 은 렌더링 함수에 전달한 context를 나타냅니다.



이제 view 에서 `list` 를 넘겨줘야합니다.

``` python
# lists/views.py

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    context = {
        'list': list_
    }
    return render(request, 'lists/list.html', context)
```



views에서 item을 넘겨주지 않으니  html도 수정을 해야합니다.

``` html
<!-- templates/lists/list.html -->

<table id="id_list_table">
    {% for item in list.item_set.all %}
        <tr><td>{{forloop.counter}}: {{ item.text }}</td></tr>
    {% endfor %}
</table>
```



