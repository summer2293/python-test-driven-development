# [chapter01] 기능 테스트를 이용한 Django 설치

### 첫 테스트

Django가 제대로 설치되었는지 사용할 준비가 되었는지 확인 하기 위해서 `셀레늄` 을 사용해서 테스트해보겠습니다.

이를 위해서 `chromedriver` 가 필요한데 해당 링크를 따라 설치 할 수 있습니다.

 https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/

``` python
# functional_test.py

from selenium import webdriver

browser = webdriver.Chrome("./chromedriver")
browser.get('http://localhost:8000')

assert 'Django' in browser.title
```



다음과 같이 테스트 결과가 실패면 준비가 완료되었습니다.

``` shell
Traceback (most recent call last):
  File "functional_test.py", line 6, in <module>
    assert 'Django' in browser.title
AssertionError
```



### Django 프로젝트 생성

책에는 `superlists` 라는 이름으로 project를 생성했지만 원래 하던대로 project와 config의 이름을 그대로 사용하겠습니다.

서버 가동 후 `functional_test.py` 을 실행하면 에러가 없어진 걸 확인할 수 있습니다.

