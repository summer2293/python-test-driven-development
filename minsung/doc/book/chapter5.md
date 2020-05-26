# [chapter05] 사용자 입력 저장하기

### POST 요청을 전송하기 위한 Form 연동

`chapter4` 마지막에 막혔던 부분을 form을 이용해서 해결해봅시다.

```html
<!-- templates/lists/home.html -->

<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
        <form method="POST" action="">
            <input name="item_text" id="id_new_item" placeholder="작업 아이템 입력" />    
            {% csrf_token %}
        </form>
        <table id="id_list_table">
        </table>
    </body>
</html>
```



### 서버에서 POST 요청 처리

`home_page` view에 적용할 새로운 단위 테스트를 만들어봅시다.

POST 요청에 대해서 반환하는 content가 `신규 작업 아이템` 을 포함하고 있는지 확인합니다.

``` python
# lists/tests.py

class HomePageTest(TestCase):
    # 생략
        

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertIn('신규 작업 아이템', response.content.decode())
```

> 테스트 코드 작성 시 줄 띄우기도 의미를 지닐 수 있습니다.
>
> 위 `test_home_page_can_save_a_POST_request` 메소드의 경우, 줄 띄우기를 기준으로 설정, 처리, 어설션 세 그룹으로 나누고 있습니다.



이를 처리하기 위해서는 다음과 같이 `views`에서도 POST 요청이 들어왔을 경우 처리를 해줘야 합니다.

하지만 이는 임시적인 처리일 뿐 궁긍적인 해결책이 될 수 없습니다.

``` python
# lists/views.py

from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    if request.method == 'POST':
        return HttpResponse(request.POST['item_text'])
    return render(request, 'lists/home.html')
```



### 파이썬 변수를 전달해서 템플릿에 출력

``` html
<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
        <form method="POST" action="">
            <input name="item_text" id="id_new_item" placeholder="작업 아이템 입력" />    
            {% csrf_token %}
        </form>
        <table id="id_list_table">
            <tr><td>{{ new_item_text }}</td></tr>
        </table>
    </body>
</html>
```



```python
def test_home_page_can_save_a_POST_request(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = '신규 작업 아이템'
    response = home_page(request)
    self.assertIn('신규 작업 아이템', response.content.decode())
```



아직 view처리가 없기 때문에 실패

```shell
self.assertEqual(response.content.decode(), expected_html)
AssertionError: '신규 작업 아이템' != '<html>\n    <head>\n        <title>To-Do [341 chars]tml>'
```



view 에서 해당 데이터를 넘겨주도록 수정하겠습니다.

``` python
# lists/views.py

from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    context = {
        'new_item_text': request.POST.get('item_text','')
    }
    return render(request, 'lists/home.html', context)
```



`test_home_page_can_save_a_POST_request` 함수를 추가해주었습니다.

이 때 html에 csrf_token을 추가하였기 때문에 문제가 발생합니다.

render_to_string에서 이를 읽지못해서 문제가 생기고 render_to_string에 request=request를 추가해주면 csrf_token은 생기지만 token값이 다릅니다.

정규 표현식을 통해 해당 부분을 제거하고 비교해주었습니다.

```python
# lists/tests.py

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
import re

def remove_csrf_tag(text):
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        # resolve를 통해 URL에 해당하는 view를 찾고 이를 실행
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('lists/home.html')

        self.assertEqual(
            remove_csrf_tag(response.content.decode()),
            remove_csrf_tag(expected_html)
        )
        

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertIn('신규 작업 아이템', response.content.decode())

        expected_html = render_to_string(
            'lists/home.html',
            {'new_item_text': '신규 작업 아이템'}
        )
        self.assertEqual(
            remove_csrf_tag(response.content.decode()),
            remove_csrf_tag(expected_html)
        )
```



현재까지 단위테스트는 문제없이 통과됩니다.

이제 기능테스트 결과를 확인해보겠습니다.

기존에 에러 메세지를 수정하여 개선할 수 있습니다.

```python
table = self.browser.find_element_by_id('id_list_table')
rows = table.find_elements_by_tag_name('tr')
self.assertTrue(
    any(row.text == '1: 공작깃털 사기' for row in rows),
    "신규 작업이 테이블에 표시되지 않는다. -- 해당 텍스트:\n%s" % (
        table.text
    )
)
```



더 나아가 해당 코드를 `assertIn` 을 통해 더 간단히 할 수 있습니다.

``` python
table = self.browser.find_element_by_id('id_list_table')
rows = table.find_elements_by_tag_name('tr')
self.assertIn("1: 공잣깃털 사기", [row.text for row in rows])
```



비록 한 줄로 줄었지만 여러 데이터를 확인하기 위해서는 같은 코드가 계속 반복됩니다.

``` python
table = self.browser.find_element_by_id('id_list_table')
rows = table.find_elements_by_tag_name('tr')
self.assertIn("1: 공잣깃털 사기", [row.text for row in rows])
self.assertIn("2: 공잣깃털을 이용하여 그물 만들기", [row.text for row in rows])
```



### 스트라이크 세 개면 리펙터

`DRY` 는 Don't Repeat Yourself 의 줄임말로서 같은 코드가 세 번 이상 등장하게 되면 중복을 제거해야 된다는 이론입니다.

이를 위해서 헬퍼메소드 `check_for_row_in_list_table`를 만들어보도록 합시다.

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome("./chromedriver")
        self.browser.implicitly_wait(3)

    def testDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
				# 생략

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table("1: 공잣깃털 사기")
        self.check_for_row_in_list_table("2: 공잣깃털을 이용하여 그물 만들기")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
```



### Django ORM과 첫 모델

하나 이상의 데이터를 처리하기 위해서는 데이터베이스가 필요합니다.

모델을 하나 만든 후 migrate를 해줍시다.

```python
# lists/models.py

from django.db import models

class Item(models.Model):
    text = models.TextField()
```



이를 테스트하기 위한 테스트 코드를 작성합시다.

``` python
# lists/tests.py

# 생략
from django.test import TestCase
from .models import Item

# 생략

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "첫 번째 아이템"
        first_item.save()

        second_item = Item()
        second_item.text = "두 번째 아이템"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "첫 번째 아이템")
        self.assertEqual(second_saved_item.text, "두 번째 아이템")
```



성공적으로 테스트가 이루어집니다.



### POST를 이용하여 데이터베이스에 저장

데이터베이스에 저장이 성공적으로 이루어지는지 확인해보도록 하겠습니다.

이를 위한 테스트 코드를 작성합니다.

``` python
# lists/tests.py

def test_home_page_can_save_a_POST_request(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = '신규 작업 아이템'

    response = home_page(request)
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, '신규 작업 아이템')

    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/')
```



다음 테스트가 성공적으로 이루어지기 위해서 `views` 에서도 데이터를 저장하고 `/` 로 redirect하도록 하겠습니다.

```python
# lists/tests.py

from django.shortcuts import render, redirect
from .models import Item

def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')
    return render(request, 'lists/home.html')
```



테스트는 성공적으로 이루어집니다.



### 테스트는 하나의 기능만을 테스트

현재 `test_home_page_can_save_a_POST_request` 에서 여러 개의 테스트가 이루어지고 있습니다.

이럴 경우 위의 테스트가 실패한 경우 아래 테스트의 성공 유무 파악이 어렵습니다.

따라서 이를 두 개로 나누어보도록 하겠습니다.

``` python
def test_home_page_can_save_a_POST_request(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = '신규 작업 아이템'

    response = home_page(request)

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, '신규 작업 아이템')

  def test_home_page_redirects_after_post(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = '신규 작업 아이템'

    response = home_page(request)

    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/')
```



### 템플릿에 있는 아이템 렌더링

`HomePageTest` 에 아래와 같은 테스트를 하나 더 추가해줍시다.

```python
def test_home_page_displays_all_list_items(self):
    Item.objects.create(text='item1')
    Item.objects.create(text='item2')

    request = HttpRequest()
    response = home_page(request)

    self.assertIn('item1', response.content.decode())
    self.assertIn('item2', response.content.decode())
```



그 후 html과 views를 고쳐줍니다.

```html
<!-- templates/lists/home.html -->

<table id="id_list_table">
    {% for item in items %}
        <tr><td>{{ item.text }}</td></tr>
    {% endfor %}
</table>
```



이제 기능 테스트를 확인해보도록 하죠.

기능 테스트를 수행하고 `localhost:8000` 을 확인해보면 기능 테스트 마다 데이터가 생성되는 것을 알 수 있습니다.

다음 두 명령어로 db를 지운 후 재성성해줍니다.

``` shell
rm db.sqlite3
python manage.py migrate --noinput
```

