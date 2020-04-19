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


--------------------------------

### 스트라이크 세개면 리팩터
같은 코드가 세번 반복 될 경우, 그 코드를 리팩터를 할 필요가 있다 
리팩터 : 코드의 기능을 수정하지 않고, 가독성이나 표현들을 수정을 한다 

--------------------------------
### 객체 관계형 맵핑 (Object-Relational Mapper ORM)
Mysql 같은 방식이라고 생각하면 편함
[ORM관련 설명 자료](https://jins-dev.tistory.com/entry/ORMObject-Relational-Mapping%EC%9D%B4%EB%9E%80-ORM-%ED%8C%A8%EB%9F%AC%EB%8B%A4%EC%9E%84%EC%9D%98-%EA%B0%9C%EB%85%90)

--------------------------------

### 데이터 베이스 
 python manage.py makemigrations 를 통해서 list/model.py에 적힌 내용을 기반으로 model을 sqlite3에 저장을 하게 됨
 
 
 
 
 
 
 





