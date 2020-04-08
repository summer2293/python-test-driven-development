## chap01 - 기능테스트를 이용한 Django 설치

#### TDD - "테스트를 작성해라"

항상 먼저 테스트를 작성한 후 실행한다. 테스트가 예상대로 실패하는지 확인한다. 이 과정이 끝나고 실제 코드를 작성한다.



#### 셀레늄 

브라우저 자동화 툴

##### functional_test.py

> 책과 다르게 폴더에 chromedriver path 를 지정해야 동작한다.. 

```
$ pip install selenium
```

```python
"""
브라우저 기능 테스트
1. 브라우저 테스트를 위한 셀레늄 설치
2. 크롬 브라우저 가동
3. 로컬 웹 PC 열기
4. 타이틀과 동일한지 assertion 생성 
"""
from selenium import webdriver # 

browser = webdriver.Chrome("./chromedriver") # 이걸 해야함..
browser.get('http://localhost:8000')

assert 'Django' in browser.title
```

shell

```python
$ python3 functional_test.py 
# result
Traceback (most recent call last):
  File "functional_test.py", line 6, in <module>
    assert 'Django' in browser.title
AssertionError
```



#### assert

assert는 뒤의 조건이 True가 아니면 AssertError를 발생한다.

```python 
>>> a = 3
>>> assert a == 2

# 결과
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```





#### django 설치

```python
$ django-admin startproject superlists
```

##### django run server

```python
$ django-admin startproject superlists
$ cd superlists
$ python3 manage.py runserver
```

##### 기능테스트 다시 실행

> 다른 쉘을 켜서 실행해보기.

```python
$ python3 functional_test.py 
$
```

아무 에러 메세지가 안나오면 성공!



#### Git 리포지토리 실행

~~생략~~ 