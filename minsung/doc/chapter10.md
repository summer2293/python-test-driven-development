# [chapter10] 입력 유효성 검사 및 테스트 구조화

사용자 입력 테스트와 유효성 검증에 대해서 다루겠습니다.



### FT 유효성 검사: 빈 작업 아이템 방지

현재 사이트는 사용자의 실수로 인해 데이터가 입력될 가능성이 있습니다. 이러한 실수를 막아주도록 합시다.

#### 테스트 건너뛰기

unittest의 skip을 사용하여 해당 테스트가 실행되지 않도록 할 수 있습니다.

```python
from unittest import skip

@skip
def test_cannot_add_empty_list_items(self):
    self.fail('write me!')
```



#### 기능 테스트 파일 분할

각 테스트를 개별 클래스로 나누겠습니다. 

기본이 되는 base.py에서 헬퍼함수들을 정의해주고 각 기능별로 새로운 파일에 새로운 클래스를 만들어 base.py의 `FuntionalTest` 을 상속받아 사용하겠습니다.

``` python
# functional_tests/base.py

# 1. LiveServerTestCase 추가
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

class FuntionalTest(StaticLiveServerTestCase):
    # 앞의 장에서 한 부분이라 나중에 보강하자.
    # @classmethod
    # def setUpClass(cls):
    #     pass
    # @classmethod
    # def testDownClass(cls):
    #     pass
    
    def setUp(self):
        # 4. ChromeDriver 변경
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3)

    def tearDown(self):
        time.sleep(3)
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
```

```python
# functional_tests/test_simple_list_creation.py

from .base import FuntionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FuntionalTest):
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

        inputbox.send_keys('공잣깃털 사기')
        inputbox.send_keys(Keys.ENTER)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공잣깃털을 이용하여 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table("1: 공잣깃털 사기")
        self.check_for_row_in_list_table("2: 공잣깃털을 이용하여 그물 만들기")

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

```python
# functional_tests/test_layout_and_styling.py

from .base import FuntionalTest


class LayoutStylingTest(FuntionalTest):
    def test_layout_and_styling(self):
        # 에디스는 메인 페이지를 방문한다.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 그녀는 입력상자가 가운데 배치된 것을 본다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
```

``` python
# functional_tests/test_list_item_validation.py


from unittest import skip
from .base import FuntionalTest


class ItemValidationTest(FuntionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        # 에디스는 빈 아이템을 실수로 등록
        # 입력상자가 비어있는 경우에 enter키

        # 페이지가 새로고침되고 빈 아이템을 등록할 수 없다는 에러

        # 다른 아이템을 입력하고 이번에는 정상 처리

        # 고의적으로 다시 빈 아이템 등록

        # 리스트 페이지에 다시 에러 메세지

        # 아이템을 입력하면 정상 동작
        self.fail('write me!')
```



다음과 같이 파일을 분리하였을 경우 아래 명령어로 모든  파일을 실행시킬 수 있습니다.

``` shell
python manage.py test functional_tests
```



각각의 파일도 따로 실행시킬 수 있습니다.

``` shell
python manage.py test functional_tests.test_list_item_validation
```



#### FT 다시 진행

``` python
# functional_tests/test_list_item_validation.py

from .base import FuntionalTest


class ItemValidationTest(FuntionalTest):
    def test_cannot_add_empty_list_items(self):
        # 에디스는 빈 아이템을 실수로 등록
        # 입력상자가 비어있는 경우에 enter키
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # 페이지가 새로고침되고 빈 아이템을 등록할 수 없다는 에러
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "빈 아이템을 등록할 수 없습니다.")

        # 다른 아이템을 입력하고 이번에는 정상 처리
        self.browser.find_element_by_id('id_new_item').send_keys('우유 사기\n')
        self.check_for_row_in_list_table('1: 우유 사기')

        # 고의적으로 다시 빈 아이템 등록
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # 리스트 페이지에 다시 에러 메세지
        self.check_for_row_in_list_table('1: 우유 사기')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "빈 아이템을 등록할 수 없습니다.")

        # 아이템을 입력하면 정상 동작
        self.browser.find_element_by_id('id_new_item').send_keys('tea 만들기\n')
        self.check_for_row_in_list_table('1: 우유 사기')
        self.check_for_row_in_list_table('2: tea 만들기')

```



예상된 에러가 발생합니다.

``` shell
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".has-error"}
```



### 모델-레이어 유효성 검증

Django에서는 두 단계로 유효성 검증을 할 수 있습니다.

하나는 모델이고, 하나는 폼(Form)입니다.

모델에서 유효성 검증을 하게 된다면 데이터베이스나 데이터베이스 무결성 규칙 부분을 직접 테스트 할 수 있습니다.

뿐만 아니라 폼을 사용하면 어떠한 폼을 사용했는지 잊어버릴 수 있지만 데이터베이스는 항상 동일한 것을 사용하기 때문에 그럴 일이 없습니다.



#### 단위 테스트를 여러 개의 파일로 리펙토링

위와 마찬가지로 단위 테스트도 두 개의 파일로 분리하도록 하겠습니다.

tests.py를 지우고 대신 tests 폴더를 만들어 그 안에 test_models.py와 test_views.py를 생성합니다.

``` python
# lists/tests/test_models.py

from django.test import TestCase
from ..models import Item, List


class ListAndItemModelTest(TestCase):
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

```python
# lists/tests/test_views.py

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
import re
from ..models import Item, List

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
    

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='item1', list=list_)
        Item.objects.create(text='item2', list=list_)

        response = self.client.get('/lists/%d/' %(list_.id,))

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')

    
    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' %(new_list.id, ))


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
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
            '/lists/%d/add_item' % (correct_list.id,),
            data={ 'item_text': '기존 목록에 신규 아이템'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

```



#### 단위 테스트 모델 유효성 검증과 self.assertRaises 컨텍스트 관리자

빈 작업 아이템을 생성하기 위한 `test_cannot_save_empty_list_items` 를 만들어 줍시다.

``` python
# lists/tests/test_models.py
from django.core.exceptions import ValidationError


class ListAndItemModelTest(TestCase):
    # 생략
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
```



다음과 같은 with 구문이 어색하게 느껴질 수 있습니다.

``` python
with self.assertRaises(ValidationError):
    item.save()
```



이는 다음과 같은 역할을 합니다.

``` python
try:
    item.save()
    self.fail('save 기능이 예외를 발생시켜야 한다.')
except ValidationError:
    pass
```



기능테스트는 다음과 같이 예상된 실패를 합니다.

``` shell
AssertionError: ValidationError not raised
```



#### 모델 저장은 유효성 검사가 되지 않는다.

우리는 Item 모델의 text 필드를 TextField로 설정하였고 이는 `blank=false` 입니다. 

하지만 text를 비우고 item을 저장해도 에러를 발생시키지 않습니다. 

이는 현재 우리가 사용하고 있는 sqlite의 문제점입니다.

sqlite의 경우, 텍스트 칼럼에 빈 값 제약을 강제화 할 수 없기 때문에 save 메소드가 빈 값을 그냥 통과 시켜버리고 맙니다.



따라서 유효성 검사를 수동으로 해줘야 합니다.

다행히 Django에서 `full_clean` 메소드를 통해 유효성 검사를 시행할 수 있습니다.

``` python
with self.assertRaises(ValidationError):
    item.save()
    item.full_clean()
```



### 뷰를 통한 모델 유효성 검증

뷰에서 모델 유효성을 검증하고 이것을 템플릿으로 가져옵시다.

우선 템플릿에서 error 데이터가 넘어온 경우 이를 표시해줍니다.

```html
<!-- templates/lists/base.html -->

<form method="POST" action="{% block form_action %}{% 
endblock %}">
    <input name="item_text" id="id_new_item" 
class="form-control input-lg" placeholder="작업 아이템 
입력" />    
    {% csrf_token %}
    {% if error %}
        <div class="form-group has-error">
            <span class="help-block">{{ error }}</span>
        </div>
    {% endif %}
</form>
```



신규 목록용 URL과 뷰가 home 페이지와 동일한 템플릿을 출력하고 에러 메세지를 출력하는지 테스트합니다.

``` python
# tests/test_views.py
from django.utils.html import escape


class NewListTest(TestCase):
    def test_validation_errors_are_sent_back_to_home_page_template(self):
    response = self.client.post('/lists/new', data={'item_text':''})
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'lists/home.html')
    expected_error = escape("You can't have an empty list item")
    self.assertContains(response, expected_error)
```



> 왜 escape를 해야하는가
>
> 서버에서 넘어온 값, `response.content.decode()` 해당 에러가 다음과 같이 넘어온다.
>
> ``` html
> <span class="help-block">You can&#39;t have an empty list item</span>
> ```
>
> django에서 아포스트로피 부분을 이스케이프 하기 때문입니다.
>
> 따라서 확인할 때 역시 escape가 필요합니다.



``` python
# lists/views.py

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html', {"error": error})
    return redirect('/lists/%d/' % (list_.id,))
```



#### 데이터베이스에 잘못된 데이터 저장 확인

현재 코드의 문제점이 존재합니다.

위의 `new_list` 를 보면 우선 item 객체를 생성한 다음에 유효성 검사를 시행합니다.

즉 유효성 검사를 실패해도 불필요한 데이터를 생성하게 되죠.



우선 단위 테스트에 불필요한 item은 저장하지 않도록 작성해봅시다.

``` python
# tests/test_views.py

class NewListTest(TestCase):
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
```



아직까지는 데이터가 생성되고 있었으므로 당연히 에러가 발생합니다.

``` python
AssertionError: 1 != 0
```



따라서 `new_list` 를 다음과 같이 수정해줍니다.

``` python
def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html', {"error": error})
    return redirect('/lists/%d/' % (list_.id,))
```



현재 FT는 실패하지만 이는 뒤에서 해결하도록 하겠습니다.

``` shell
python manage.py test functional_tests.test_list_item_validation 
```

```shell
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".has-error"}
```



### 폼 렌더링 뷰와 같은 뷰에서  POST 요청 처리

이번에는 다른 방법으로 접근해봅시다.

폼 랜더링에 사용하는 뷰에서 POST 요청을 처리하는 방식으로 RESTful 모델에 적합하지는 않지만 동일 URL에서 폼 뿐만 아니라 사용자 입력 처리 시 발생하는 에러도 출력한다는 이점이 있습니다.

URL을 하나로 합치기 위해 우선  list.html의 action을 수정합시다. 

``` html
<!-- templates/lists/list.html -->

{% block form_action %}
/lists/{{list.id}}/
{% endblock %}
```



#### new_item의 기능을 new_list로 리팩터링

기존 `NewItemTest`의 모든 테스트를 `ListViewTest`로 옮기고 `NewItemTest`은 삭제해줍시다.

각각에 대해 요청  URL을 변경해주었고, `test_redirects_to_list_view` 은 `test_POST_redirects_to_list_view` 다음과 같이 이름을 변경하였습니다.

``` python
# lists/tests/test_views.py

class LiveViewTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data = {'item_text': '기존 목록에 신규 아이템'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '기존 목록에 신규 아이템')
        self.assertEqual(new_item.list, correct_list)

    
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={ 'item_text': '기존 목록에 신규 아이템'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
```



이제 `view_list` 를 수정하여 두 가지 요청을 처리할 수 있도록 합시다.

```python
# lists/views.py

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/lists/%d/' %(list_.id,))
    context = {
        'list': list_
    }
    return render(request, 'lists/list.html', context)
```



이제 `add_item` 은 필요없어졌으니  view에서 지우고 urls에서도 지워줍시다.

이제 기능테스트는 문제 없이 모두 작동합니다.



#### view_list에서 모델 유효성 검증 구현

모델 검증 규칙에 맞춰서 기존 리스트에 아이템을 추가하는 처리를 해보겠습니다.

이를 위한 단위테스트 입니다.

```python
# tests/test_views.py

class LiveViewTest(TestCase):
    # 생략
    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
```



뷰가 아직 유효성 검사를 시행하고 있지 않기 때문에 이를 추가해줍시다.

``` python
# tests/views.py

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect('/lists/%d/' %(list_.id,))
        except ValidationError:
            error = "You can't have an empty list item"

    context = {
        'list': list_,
        'error': error
    }
    return render(request, 'lists/list.html', context)
```



단위테스트가 성공적으로 이루어집니다.

기능테스트도 마찬가지로 성공적으로 이루어진다.

> 만약 기능테스트가 성공적으로 이루어지지 않는다면
>
> 같은 코드임에도 불구하고 기능테스트가 다른 부분에서 에러를 발생하였습니다. 분명히 잘못된 부분이 없었고 디버깅을 해봐도 테스트를 통과해야 했습니다.
>
> 책 앞부분에 나왔듯이 sleep을 걸어 잠시 대기하게 되면 코드가 통과되는걸 확인할 수 있었습니다. 
>
> 이를 암시적 대기, Implicit Wait라고 했었죠.
>
> 하지만 이는 비효율적입니다. 
>
> 이럴 때 사용하는게 명시적 대기, Explicit Wait 입니다.
>
> 최대 시간을 정하고 해당 시간이 되거나 원하는 값을 찾으면 대기를 종료하는 방식인데 뒤에서 다시 다룰 것이기 때문에 우선은 암시적 대기로 테스트를 진행하겠습니다.



#### 하드코딩된  URL 제거

우선  urls의 각  endpoint에 이름을 지정해주겠습니다.

``` python
# lists/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('lists/<int:list_id>/', views.view_list, name='view_list'),
    path('lists/new', views.new_list, name='new_list'),
]
```



#### {% url %} 템플릿 태그

각 html의 url을 탬플릿 태그를 이용하여 리펙토링하겠습니다.

``` html
<!-- templates/lists/home.html -->

{% block form_action %}
{% url 'new_list' %}
{% endblock %}


<!-- templates/lists/list.html -->

{% block form_action %}
{% url 'view_list' list.id %}
{% endblock %}
```



#### get_absolute_url을 이용한 리다이렉션

우선 views에서도 endpoint의 name을 통해 리펙토링합시다.

``` python
# lists/views.py

def view_list(request, list_id):
    # 생략
    return redirect('view_list', list_id)
  
def new_list(request):
    # 생략
    return redirect('view_list', list_.id)
```



`get_absolute_url`을 이용하기 위해서 잘 동작하는지 유닛테스트 함수를 작성해줍시다.

```  python
# lists/tests/test_models.py

class ListAndItemModelTest(TestCase):
    # 생략
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' %(list_.id, ))
```



해당 model에 다음과 같이  `get_absolute_url`이 존재해야 합니다.

``` python
# lists/models.py

from django.urls import reverse

class List(models.Model):
    pass

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])
```



이 경우 redirect를 할 시 , 자동적으로 `get_absolute_url` 에 해당 객체를 넣어 redirect하게 됩니다.

```python
# lists/views.py

def view_list(request, list_id):
    # 생략
    return redirect(list_)
  
def new_list(request):
    # 생략
    return redirect(list_)
```



현재 유닛테스트와 기능테스트 모두 무사히 성공합니다.