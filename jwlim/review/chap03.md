### Chap03 : 단위 테스트를 이용한 간단한 홈페이지 테스트  


#### 1. 정리
* Unit Test (UT) vs Functional Test (FT)    
둘의 기본적인 차이는 FT는 사용자 관점에서 애플리케이션 외부를 테스트하는 것이고, UT는 프로그래머 관점에 그 내부를 테스트한다는 것이다.
책에서는 TDD를 양쪽 테스트 모두에 적용한다.  
    작업의 순서  
    1. FT를 작성해서 사용자 관점의 새로운 기능성을 정의한다.
    2. FT를 실패하고, 어떻게 작성해야 테스트를 통과할지 생각한다. 그리고 UT를 이용해서 어떻게 코드가 동작해야하는지 정의한다.
    3. UT가 실패하고 나면 UT를 통과할 수 있을 정도의 최소한의 코드만 작성한다.
    4. FT를 재실행해서 통과하는지 또는 제대로 동작하는지 확인한다. (이때 새로운 UT를 작성해야 할 수도 있다)

* Django에서의 단위 테스트  
`from django.test import TestCase`

* Django의 MVC, URL, 뷰 함수
Django는 Model-View-Controller 패턴을 따름.
따라서, Django의 처리 흐름은 아래와 같다.
1. 특정 URL에 대한 HTTP 요청(request)을 받는다.
2. Django는 특정 규칙을 이용해서 해당 요청에 어떤 뷰 함수를 실행할지 결정한다. (URL 해석)
3. 이 뷰 기능이 요청을 처리해서 HTTP 응답(response)으로 반환한다.

#### 2. 책 이외로 알아본 것  

