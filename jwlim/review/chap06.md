### Chap06 : 최소 동작 사이트 구축  


#### 1. 정리
* 기능 테스트 내에서 테스트 격리
    * 기능 테스트를 실행할 때마다, 앞 테스트의 결과물이 데이터베이스에 남아있다. -> 다음 테스트 결과 해석을 방해한다.
    * 단위 테스트를 실행하면, Django 테스트 실행자가 자동으로 새로운 (별도의) 테스트 데이터베이스를 생성한다.
* 필요한 경우에는 최소한의 설계를
    * TDD와 Agile 개발
        * 동작하는 최소한의 애플리케이션을 빠르게 만들고, 이를 이용해서 얻은 실제 사용자 의견을 설계에 점진적으로 반영해 가는 것
    * YAGNI (You ain't gonna need it)
        * 설계에 대해 한번 시작하면, 이것저것 붙여서 완벽하게 만들고 싶어진다, 하지만 이런 마음을 참고 당장 필요한 것만 만들어야한다.  
    * REST (Representational State Transfer)
        * 웹 기반 API를 이용하는 웹 설계 방법 중 하나이다.
        * REST는 데이터 구조를 URL 구조에 일치시키는 방식이다.
            * ex) /lists/<목록 식별자>/
            * ex) /lists/new
            * ex) /lists/<목록 식별자>/add_item
    * TDD를 이용해서, 새로운 설계를 반영하기
        ![기능 테스트와 단위 테스트를 이용한 TDD처리](chap06_img_01.png)
        * 상위 layer에서 신규 기능 추가(FT를 확장하고 새로운 애플리케이션 코드를 작성)하고, 앱 리팩터링한다.
        * 단위 테스트 계층에선 신규 테스트를 추가하거나 기존 것을 수정해서 변경사항을 테스트한다.
    * 동작 상태 확인 후 다음 동작 상재 확인 -> Testing Goat VS Refactoring Cat
        * Testing Goat(한 단계씩 수정해서 동작하는지 확인 후 다음 단계 진행)보다 일반적으로 모든 것을 한 번에 수정하는 것이 쉽다. 
        하지만 주의하지 않으면 결국 Refactoring Cat(욕조에 빠져 나오지 못하는 고양이)처럼 오히려 많은 코드를 재수정해야 하거나, 
        아무것도 동작하지 않는 상태가 된다.
    
#### 2. 책 이외로 알아본 것
* python raw string
    * python의 r''은 string을 raw string으로 읽는다는 것이다.
    * > 'Hi\nHello'  
        Hi  
        Hello  
    * > r'Hi\nHello'  
        ~~Hi\nHello~~ : Unicode Error  
    * > r'Hi\xHello'  
        'Hi\\xHello'    
         
* 정규 표현식
    * ^ : Not
    * d : 숫자 [0-9]
    * 0 : 0번이상 반복
    * '+' : 1번이상 반복
    * {} : 횟수 표시
    * $ : End of string, or end of line  
    
* Django urlpattern
    * django.conf.urls import patterns, url VS django.urls import path, include, re_path
        * url == re_path  
            