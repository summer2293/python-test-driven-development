# [chapter07] 멋있게 만들기: 레이아웃, 스타일링, 테스트

현재까지 만든 사이트를 출시하기 위한 준비작업을 해보도록 하겠습니다.

이번 장에서는 여러 준비작업 중, 스타일링 방법에 대해서 알아보겠습니다.



### 레이아웃과 스타일을 기능적으로 테스트하기

* 신규 및 기존 목록 추가를 위한 크고 멋있는 입력 필드
* 크고 시선을 끄는 중앙 입력 박스

스타일링을 위해 CSS를 사용할텐데 이 CSS는 정적파일로 로딩이 됩니다. 이는 호스팅 서비스에서는 다루기 힘들 수 도 있는데 이를 위해 `스모크 테스트`를 이용하도록 하겠습니다.



먼저 기능테스트를 하기 위해 새로운 테스트 메소드를 추가합시다.

해당 테스트는 먼저 창 크기를 고정시키고 시작합니다. 

그리고 입력 요소를 찾은 후 계산을 해줍니다. 

`assertAlmostEqual` 에서 `delta` 값을 지정해주면 비교하는 두 값이 플러스/마이너스 delta 값 만큼 허용해줍니다.

``` python
# functional_tests/tests.py

class NewVisitorTest(LiveServerTestCase):
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



예상한대로 결과는 실패입니다.

아직 inputbox의 위치는 좌측에 있으니까요.

``` shell
AssertionError: 73.5 != 512 within 10 delta (438.5 difference)
```



이런 종류의 FT는 잘못된 방향으로 가기 쉽기 때문에 빠르긴 하지만 지저분한 '편법'을 사용하겠습니다. 

이를 통해 inputbox가 가운데 있으면 FT가 통과되게 할 수 있습니다.

``` html
<!-- templates/lists/home.html -->
```



### 멋있게 만들기: CSS 프레임워크 이용

CSS를 적용하기 위해서 CSS 프레임워크 Bootstrap을 적용해보도록 하겠습니다.

간단하게 CLI로 bootstrap 파일을 다운받고 압축해제 해주도록 하겠습니다.

``` shell
wget -O bootstrap.zip https://github.com/twbs/bootstrap/releases/download/v3.1.0/bootstrap-3.1.0-dist.zip
unzip bootstrap.zip
mkdir lists/static
mv dist lists/static/bootstrap
rm bootstrap.zip
```



이제 다운받은 bootstrap을 적용해봅시다.

하지만 현재 존재하는 두 개의 html파일에 각각 link태그와 script태그를 적용하는 것은 비효율적입니다.

Django template 상속을 이용하겠습니다.

`base.html` 를 만들어주고 아래와 같이 입력합니다.

``` html
<!-- lists/base.html -->

<html>
    <head>
        <title>To-Do lists</title>
        <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
    </head>
    <body>
        <div class="container">
            <div class="row">
                <div class="col-md-6 col-md-offset-3">
                    <div class="text-center">
                        <h1>{% block header_text %}{% endblock %}</h1>
                        <form method="POST" action="{% block form_action %}{% endblock %}">
                            <input name="item_text" id="id_new_item" placeholder="작업 아이템 입력" />    
                            {% csrf_token %}
                        </form>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 col-md-offset-3">
                    {% block table %}
                    {% endblock %}
                </div>
            </div>
        </div>
    </body>
</html>
```



이제 이를 상속받아 `home.html`과` list.html`도 수정해줍시다.

```html
<!-- lists/home.html -->

{% extends './base.html' %}

{% block header_text %}
작업 목록 시작
{% endblock %}

{% block form_action %}
/lists/new
{% endblock %}


<!-- lists/list.html -->

{% extends './base.html' %}

{% block header_text %}
Your To-Do list
{% endblock %}

{% block form_action %}
/lists/{{list.id}}/add_item
{% endblock %}

{% block table %}
<table id="id_list_table">
    {% for item in list.item_set.all %}
        <tr><td>{{forloop.counter}}: {{ item.text }}</td></tr>
    {% endfor %}
</table>
{% endblock %}
```



FT를 실행해보면 아직 css가 적용되지 않아서 문제가 생기는 것을 알 수 있습니다.

``` shell
AssertionError: 73.5 != 512 within 10 delta (438.5 difference)
```



### Django 정적파일

django 뿐만 아니라 일반 웹서버에서는 정적 파일을 다루기 위해서 다음 두 가지 사항을 고려해야 합니다.

1. URL이 정적 파일을 위한 것인지 뷰 함수를 경유해서 제공되는 HTML을 위한 것인지 구분 할 수 있는가
2. 사용자가 원할 때 어디서 정적 파일을 찾을 수 있는가



첫번째를 위해서 Django에서는 URL 접두사를 정의합니다.

특정 접두사로 시작하는 URL은 정적 파일을 위한 요청이라고 인식을 하는 것이죠.

settings를 확인하면 `/static/` 이라는 이름으로 초기 설정이 되어있습니다.

```python
# config/settings.py

STATIC_URL = '/static/'
```



첫번째는 기본 세팅으로 해결이 되었으니 두 번째에 대해서 알아봅시다.

`python manage.py runserver` 를 통한 Django 개발 서버를 이용하는 동안 Django는 각 앱의 서브폴더 속 `static` 이라는 폴더를 찾음으로서 정적 파일을 찾을 수 있습니다. 

마찬가지로 `boostrap` 관련 파일도 `lists/static` 경로에 있는데 왜 읽지 못하는 것일까요?

원인은 위에서 설명한 첫번째에 있습니다. 

현재 경로를 확인해보면 URL에 static이 없습니다.

즉 django는 이를 정적파일을 위한 것인지 인식을 못하는 것이죠.

``` html
<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
```



따라서 다음과 같이 수정해줍시다.

```html
<link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
```



이제 CSS가 적용되는 것을 확인할 수 있습니다. 



#### StaticLiveServerTestCase

하지만 아직까지 FT는 같은 이유로 실패합니다.

왜 CSS가 적용되었는데 FT에서는 인식을 못할까요?

이는 근본적으로 `LiveServerTestCase` 에 있습니다. 

이를 위해 `LiveServerTestCase` 대신 `StaticLiveServerTestCase` 를 사용하겠습니다.

``` python
# fuctional_tests/tests.py

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):
    # 생략
```



이제 FT를 통과하는 걸 확인할 수 있습니다.



### 부트스트랩 컴포넌트를 이용한 사이트 외형 개선

* 점보트론을 이용한 강조
* 큰 입력 상자
* 테이블 스타일링

``` html
<!-- lists/base.html -->

<div class="col-md-6 col-md-offset-3 jumbotron">
    <div class="text-center">
        <h1>{% block header_text %}{% endblock %}</h1>
        <form method="POST" action="{% block form_action %}{% endblock %}">
            <input name="item_text" id="id_new_item" 
class="form-control input-lg" placeholder="작업 아이템 입력" />    
            {% csrf_token %}
        </form>
    </div>
</div>
          
<!-- lists/list.html -->          
<table id="id_list_table" class="table">
```



### 사용자 지정 CSS 사용하기

``` html
<!-- lists/base.html -->

<link href="static/base.css" rel="stylesheet" media="screen">
```

```css
// lists/static/base.css

#id_new_item {
    margin-top: 2ex;
}
```

> LESS란? 
>
> LESS는 CSS에 Script의 능력(변수, 함수, 연산, 중첩, 스코프등등)을 덧붙여 확장한 언어이다.



이제는 FT를 모두 통과하는 물론 겉보기에도 꽤나 그럴 듯한 페이지가 완성되었습니다. 



### collectstatic과 다른 정적 디렉터리

위에서 언급했듯이 Django 개발 서버를 이용하는 동안 Django는 각 앱의 서브폴더 속 `static` 이라는 폴더를 찾음으로서 정적 파일을 찾을 수 있습니다. 

하지만 실제 운영중인 웹서버에서는 Django가 정적 콘텐츠를 제공하는 것이  매우 느리며 비효율적입니다. 

따라서 Apache나 Nginx같은 웹서버를 통해 다음과 같은 과정을 거치기도 합니다. 

따라서 여러 앱에 존재하는 모든 정적파일을 한 곳에 모아서 배포용으로 관리를 해야할 필요가 있습니다.

Django에서는 이를 collectstatic 명령으로 가능하게 합니다.

그리고 파일들을 모을 위치는 settings.py에 `STATIC_ROOT`를 통해 설정가능합니다. 

```python
# config/settings.py

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))
```



경로를 보면 `BASE_DIR` 인 project 보다 상위 폴더에 `static` 폴더를 만들어 모으는 것을 확인할 수 있습니다.

각 앱의 `static` 안에 이미 존재하는 파일들을 복사해서 모으기만 하는 것이기 때문에 코드 관리를 해줄 필요가 없어 밖에 위치시킵니다.



> 디자인 레이아웃 테스트
>
> 디자인과 레이아웃용 테스트는 작성할 필요가 없습니다.
>
> 이 말의 뜻은 각각의 디자인에 대한 세세한 테스트를 작성할 필요가 없다는 뜻으로 디자인과 레이아웃이 동작하고 있다는 것을 확실할 수 있게 해주는 최소한의 테스트만을 작성하자는 의미입니다.
>
> 위에서 본 것과 같이 가운데에 위치하는지 확인하는 식으로 말이죠.