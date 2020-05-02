### Chap07 : 멋있게 만들기: 레이아웃, 스타일링, 테스트  



#### 1. 정리

 * 레이아웃과 스타일을 기능적으로 테스트하기

   	* functional_test.py에 test_layout_and_styling 함수를 작성하였다.

 * 멋있게 만들기: CSS 프레임워크 이용

   	* https://getbootstrap.com/
   	* 부트스트랩 : 트위터에서 시작된 jQuery 기반의 오픈 소스 프론트엔드 라이브러리

 * Django 템플릿 상속

 * 부트스트랩 통합하기

 * Django의 정적파일

 * 부트스트랩 컴포넌트를 이용한 사이트 외형 개선

    * Jumbotron 클래스를 사용해서, 메인 페이지의 헤더와 입력 폼을 강조함

 * 사용자 지정 CSS 사용하기

 * 얼버무리고 넘어간 것: collectstatic과 다른 정적 디렉터리

    * Django가 정적 콘텐츠를 제공하도록 하는 것은 느리고 따라서 비효율적임 (Apache, Nginx 웹 서버가 대체할 수 있음. 또는 CDN(Content Delivery Network)에 업로드해서 호스팅하는 방법도 있음.)
    * 따라서, 위와 같은 이유로 여러 앱에 존재하는 모든 정적 파일을 한 곳에 모아서 배포용으로 만들어주는 것이 collectstatic 커맨드이다.

 * 정리

    * 디자인과 레이아웃용 테스트는 작성할 필요가 없다. (이것은 상수를 테스트하거나 취약성이 있을만한 것을 테스트를하는 것과 같다.)

    * 디자인 및 레이아웃 구현은 CSS와 static 파일을 가지고 있다. 따라서, CSS파일과 static 파일이 동작하는지만 확인하는 것이 좋다.

      

#### 2. 책 이외로 알아본 것



#### 3. 의논하고 싶은 것
* 책 처럼 111.0 != 512가 되지 않음.

  ```python
  def test_layout_and_styling(self):
      # 에디스는 메인 페이지를 방문한다
      self.browser.get(self.live_server_url)
      self.browser.set_window_size(1024, 768)
  
      # 그녀는 새로운 리스트를 시작하고 입력 상자가
      # 가운데 배치된 것을 확인한다
      inputbox = self.browser.find_element_by_id('id_new_item')
      # inputbox.send_keys('testing\n')
      # inputbox.send_keys(Keys.ENTER)
      self.assertAlmostEqual(
          inputbox.location['x'] + inputbox.size['width'] / 2, # 272.5
          # 512,
          265,
          delta=10
      )
  ```

