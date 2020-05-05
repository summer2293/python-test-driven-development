## chap07. 멋있게 만들기. 레이아웃, 스타일링, 테스트

### 요약

#### StaticLiveServerTestCase

> 이전에 사용하던 liveservertest를 사용할경우 자동으로 정적파일을 찾을 수 없다. 
> 정적 파일을 사용할경우, 이때는 TestCase 서브 클래스를 확장한 도구인 __StaticLiveServerTestCase__ 를 사용한다. 
>
> https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
>
> 

#### 디자인 레이아웃 테스트

> - 디자인과 레이아웃용 테스트는 작성할 필요가 없다. 상수를 테스트하는 것과 같다.
>
> - 최소한 의 “스모크 테스트”를 이용해서 CSS와 정적 파일이 동작하는지만 확인하자. css 정적 파일이 동작하는지 확인하면, 서버 배포시 발생할 수 있는 문제를 찾을 수 있다. 
>
>   ###### 스모크 테스트
>
>   테스트 수행 전, 테스트 대상이나 제품의 빌드가 구축된 테스트 환경에서 테스트가 가능한지 판단하는 테스트. 
>



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

오류가 안 잡힌다 ㅠ

https://stackoverflow.com/questions/34629261/django-render-to-string-ignores-csrf-token/39859042#39859042

삽질기 

- name 안붙혀서 error



```
tddjango/superlists/functional_tests/tests.py", line 94, in test_layout_and_styling
    self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10)
AssertionError: 315.0 != 512 within 10 delta (197.0 difference)
```

어떻게 잡으셨나요..



## 이해가 안가는 내용

x



## 참조 사이트 

> https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
>
> https://zinee-world.tistory.com/131
>
> https://getbootstrap.com/docs/4.0/components/jumbotron/