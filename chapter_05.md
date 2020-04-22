CSRF(cross-site Request Forgery) 공격
``` html
<form>
  {% csrf_token %}
  <input type="text" name="text"/>
  <input type="submit" value="확인"/>
</form>

```

클라이언트에서 해당 페이지를 접속하게 되면 Django 에서 자동으로 csrf_token을 클라이언트로 보내어 cookie에 저장시키고, POST로 전송할 때 cookie의 csrf_token 이 함께 전송되어 인증하는 방식이다
  아래와 같은 공격을 막을 수 있다.

CSRF 공격이란?
CSRF 공격(Cross Site Request Forgery)은 웹 어플리케이션 취약점 중 하나로, 인터넷 사용자(희생자)가 자신의 의지와는 무관하게 공격자가 의도한 행위(수정, 삭제, 등록 등)를 특정 웹사이트에 요청하게 만드는 공격
출처: (https://velog.io/@ground4ekd/django-csrf)[https://velog.io/@ground4ekd/django-csrf]

-----------------------------------

```python
table = self.browser.find_element_by_id("id_list_table") #find_element_by_id -> find_element_by_id
rows = table.find_elements_by_tag_name("tr") # eldments 와 element의 차이로도 에러가 날 수 있음
self.assertIn("1: 공작깃털 사기", [row.text for row in rows])


ERROR: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitor)
Traceback (most recent call last):
  File "chapter_05.py", line 41, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn("1: 공작깃털 사기", [row.text for row in rows])
TypeError: 'WebElement' object is not iterable
```
이런 경우가 나타 날 경우, 
**Solution: replace find_element_by_xpath with find_elements_by_xpath**

 출처: (https://stackoverflow.com/questions/39520426/typeerror-webelement-object-is-not-iterable-error)[https://stackoverflow.com/questions/39520426/typeerror-webelement-object-is-not-iterable-error]

-------------------------------

```python
Django
def hoem_page(request):
  return render(request, "home.html",{
    'new_item_text' : request.POST.get("item_text","")
  })
```

```python
Flask
@app.route('/test', methods=['POST'])
def test():
    # save image file and bytes
    image_file = request.files["image"]
    image_file_name = image_file.filename
```
이런 식으로 다르게 받는게 신기하네요

-------------------------------
Template 언어란?
```python
Django
def hoem_page(request):
  return render(request, "home.html",{
    'new_item_text' : request.POST.get("item_text","")
  })
```
이와 같은 입력에 대해서, home.html에 
{{ new_item_text }} 와 같은 방식으로 html에 내부에서 접근을 가능케 하는 방식이다


--------------------------------

### 스트라이크 세개면 리팩터
같은 코드가 세번 반복 될 경우, 그 코드를 리팩터를 할 필요가 있다 
리팩터 : 코드의 기능을 수정하지 않고, 가독성이나 표현들을 수정을 한다 

--------------------------------
### 객체 관계형 맵핑 (Object-Relational Mapper ORM)
Mysql 같은 방식이라고 생각하면 편함
[ORM관련 설명 자료](https://jins-dev.tistory.com/entry/ORMObject-Relational-Mapping%EC%9D%B4%EB%9E%80-ORM-%ED%8C%A8%EB%9F%AC%EB%8B%A4%EC%9E%84%EC%9D%98-%EA%B0%9C%EB%85%90)


 ```python
from django.db import models
# Create your models here.
# models.Model 을 상속 해야 이런 .save(), .objects() 같은 함수들을 쓸수 있다
class Item(models.Model):
    text = models.TextField(default='')
```

[장고에서 모델을 정의를 하고 사용하는 법](https://wayhome25.github.io/django/2017/03/20/django-ep5-model/)

 ```python
# 2. shell에서 migrations, migrate 실행
$ python3 manage.py makemigrations
$ python3 manage.py migrate
# 위 명령을 통해서 앱폴더 아래에 migration 폴더가 생성되고 DB에 테이블을 생성한다.
```

[마이그레이션을 하는 이유](https://wayhome25.github.io/django/2017/03/20/django-ep6-migrations/)


--------------------------------

### 데이터 베이스 
 python manage.py makemigrations 를 통해서 list/model.py에 적힌 내용을 기반으로 model을 sqlite3에 저장을 하게 됨
 
 django.db.utils.OperaionalError: no such column: list_item.text 가 뜬다면, 
 
 
 ```python
python manage.py makemigrations 

or

rm db.slite3
python mange.py makemigrations 
python manage.py migrate --noinput 
이렇게 진행을 하는것이 좋아보인다

```
 ---------------------------------------
 .object.create 는 .save()의 축약 명령으로 호출이 필요 없다 
 
 
 ```python
def home_page(request):
  item = Item()
  item.text = request.POST.get("item_text","")
  item.save()
  
or 
def home_page(request):
  if request.method == "POST":
    new_item_text = request.POST['item_text']
    Item.objects.create(text = new_item_text)
  else:
    new_item_text = ""
  return render(request, 'home.html',{
    'new_item_text' : new_item_text
  })
```

그리고
```python
request.POST.get("item_text","")
or 
request.POST["item_text"]
``` 
두방식 모두 쓸수 있지만 각각의 경우가 있으므로, 아래 포스트에 정리를 해두었길래 들고 왔습니다 
[https://cjh5414.github.io/django-keyerror/](https://cjh5414.github.io/django-keyerror/)

 
 
 -------------------------------------------
 http status code 를 보다가 절학히 무었을 정의하는지 궁금해서 찾아 보았고,
 아래 링크로 가면 있습니다.
200 : 요청은 정상이고, 본문은 요청된 리소스를 포함하고 있다.  
301 : 요청한 URL이 옮겨졌을 때 사용. 옮겨진 URL에 대한 정보와 함께 응답되어야 한다.  
302 : 301과 동일하나, 클라이언트는 여전히 옮겨지기전 URL로 요청할것을 의미  
 [http status code 정리 ](https://velog.io/@honeysuckle/HTTP-%EC%83%81%ED%83%9C-%EC%BD%94%EB%93%9C-HTTP-status-code-)
 
 
 





