## chap01 - 기능테스트를 이용한 Django 설치

#### 셀레늄 

브라우저 자동화 툴

##### functional_test.py

> 책과 다르게 폴더에 chromedriver path 를 지정해야 동작한다.. 

```python
"""
브라우저 기능 테스트
1. 브라우저 테스트를 위한 셀레늄 설치
2. 크롬 브라우저 가동
3. 로컬 웹 PC 열기
4. 타이틀과 동일한지 assertion 생성 
"""
from selenium import webdriver # 

browser = webdriver.Chrome("./chromedriver")
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