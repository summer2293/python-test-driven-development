## chap10. 입력 유효성 검사 및 테스트 구조화 

### 요약

#### ft - 유효성검사

빈 값 또는 두번 입력하는 유효성 방지하기 

> 기능 테스트는 사용자 스토리와 밀접한 관련이 있다. 하나의 티켓은 여러 사용자 스토리를 포함한다. 또한 각 기능이 하나의 파일 또는 클래스로 구성되며, 각 사용자 스토리는 여러 메서드로 구성된다.


## 새로 알게 된 점

##### ex

> html/css 많이 해봐서 px오타인줄 알았는데 ex라는 문법이 있었다. 
>
> \- ex : x-height, 해당폰트의 소문자 x의 높이를 기준으로 함.
> \- px : pixel, 표시장치(모니터)에 따라서 상대적인 크기를 가짐.
>
> https://zinee-world.tistory.com/131

```css
#id_new_item {
  margin-top: 2ex;
}
```

##### jumbotron

> 부트스트랩에서 한번도 안써봐서 신기했음
>
> https://getbootstrap.com/docs/4.0/components/jumbotron/



## 같이 이야기 하고 싶은 내용

##### 수민 - 오류가 안 잡힌다 ㅠ

https://stackoverflow.com/questions/34629261/django-render-to-string-ignores-csrf-token/39859042#39859042

삽질기 

- name 안붙혀서 error



```
tddjango/superlists/functional_tests/tests.py", line 94, in test_layout_and_styling
    self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10)
AssertionError: 315.0 != 512 within 10 delta (197.0 difference)
```

어떻게 잡으셨나요..



##### 지수 - 논의 사항

- `StaticLiveServerCase` 가 아니고 `StaticLiveServerTestCase` 가 맞음

- django admin 지우니까 서버가 안돌아감...?
- static 폴더를 밖으로 빼고 collectstatic 했는데 테스트는 적용이 안되고 서버 돌린거는 적용이 된다. 뭐지?



## 이해가 안가는 내용





## 참조 사이트 

> https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
>
> https://zinee-world.tistory.com/131
>
> https://getbootstrap.com/docs/4.0/components/jumbotron/