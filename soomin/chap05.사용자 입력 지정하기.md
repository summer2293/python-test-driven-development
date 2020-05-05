## chap05. 사용자 입력 지정하기

### 목표
> 시스템 설계. 여러 목록과 각 목록별 작업 아이템을 만들고, url을 적용한다. 

## 요약 

#### 기능 테스트 에러 시 사용하는 방법

- print
- error message 개선
- 수동으로 site open
- time sleep




### 레드 / 그린 / 리펙터와 삼각법

- 실패 할 단위테스트 (read)
- 통 과할 최소코드 작성. 편법 가능(green)
- 리팩터링 해서 이해할 수 있는 코드 작성 
  
  > 리팩토링 시, 편법을 허용하지 않게 확장한다.

### 띄어쓰기

필자는 테스트 설정을 위한 세 줄의 코드를 한 그룹으로 묶고, 그 다음은 실제 함수를 호출하는
코드 부분(가운데 한 줄), 그리고 마지막 부분을 어설션으로 구성해서 세 개 그룹으로 나누고 있다. 

이것은 강제사항은 아니지만 테스트 구조를 쉽게 파악할
수 있도록 도움을 준다. 설정(Setup), 처리(Exercise), 어설션(Assert)은 단위 테 스트의 전형적인 구조다.

> give, when, then 으로 사용하는거랑 비슷한듯

### 각 테스트는 하나의 기능만 테스트 해야한다.

- bug tracing 이 유리해진다.
- test assert 로 상태 파악을 가능할 수 있다. 



## ETC 

### csrf error

Django의 CSRF 보호는 사이트의 각 폼이 생성하는 POST 요청을 확인할 수 있는 토 큰을 자동 생성한다. 지금까지는 순수 HTML로 이루어진 템플릿을 사용했지만, 이제 부터는 Django의 템플릿 마술을 적용하도록 한다. CSRP 토큰을 추가하기 위해 템플 릿 태그를 이용한다.



#### ORM

객체 관계형 맵핑(Object-Relational Mapper, ORM) 

이것을 이용하면 익숙한 객체 지향 코딩 방식을 이용해서 데이터베이스를 처리할 수 있다. 데이터베이스는 클래스로 표현하고, 컬럼은 속성, 레코드는 각 클래스의 인스턴스로 표현한다.



## 새로 알게 된 점



## 같이 이야기 하고 싶은 내용

csrf오류 re 외에는 답이 없는가?

https://stackoverflow.com/questions/34629261/django-render-to-string-ignores-csrf-token/39859042#39859042

삽질기 

- name 안붙혀서 error



## 이해가 안가는 내용





## 참조 사이트 
> https://laravel.com/docs/7.x/csrf
> https://docs.djangoproject.com/en/dev/ref/csrf/#testing
