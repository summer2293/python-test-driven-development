### Chap02 : unittest 모듈을 이용한 기능 테스트 확장  


#### 기능 테스트를 이용한 최소 기능의 애플리케이션 설계  
* 기능 테스트 == 승인 테스트 == 종단간 테스트  
* (Functional Test == Acceptance Test == End-to-End Test)  
* FT는 프로그래머가 아니더라도 이해할 수 있어야 한다는 것  

#### unittest.TestCase  
* test로 시작하는 모든 메소드는 테스트 메소드이다.
* setUp, tearDown **&larr;** **&rarr;** try/except  
* assert **&rarr;** self.assertIn : 전체 문장에서 내가 찾으려는 문장이 있는가  
