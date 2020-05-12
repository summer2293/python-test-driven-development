### Chap10 : 입력 유효성 검사 및 테스트 구조화  



#### 1. 정리

 * 테스트 건너뛰기

     * unittest의 skip decorater를 사용하여 테스트를 생략한다.

     * ```python
        from unittest import skip
        ```
     
 * 기능 테스트를 여러 파일로 분할, 하나의 파일이 하나의 클래스를 이용하게 바꿈

      * base 파일을 만들고 상속을 하는 방식으로 이용함.

 * 모델-레이어 유효성 검증 : Django에서는 두 단계로 유효성 검증을 함

      * 한 개는 모델 계층, 다른 하나는 상위 계층에 있는 Form이다.
      * https://jay-ji.tistory.com/32
      * Form Class : HTML Form을 좀 더 쉽게 만들 수 있게 해주고, 직접 필드 정의
      * Model Class :  Model과 필드를 지정하면, 자동으로 Form 필드를 생성, 데이터 베이스 무결성 규칙 부분을 직접 테스트 가능

 * 뷰를 통한 모델 유효성 검증

      * 사용자가 유효성 검증을 확인할 수 있다. (HTML로 에러를 표시)

 * 데이터베이스에 잘못된 데이터가 저장됐는지 확인

 * Django 패턴 : 폼 렌더링 뷰와 같은 뷰에서 POST 요청 처리

 * get_absolute_url



#### 2. 의논하고 싶은 것
* 책 208pg : 수상한 Django: 모델 저장은 유효성 검사가 되지 않는다.

  * Save 메소드가 빈 값을 통과시키지 않는다.
  
  ```python
  with self.assertRaises(ValidationError):
    item.save()
    item.full_clean()
  ```

  * 책 212pg : 에러가 발생하지 않음
  
  ```python
  expected_error = escape("빈 아이템을 등록할 수 없습니다")
  print(response.content.decode())
  self.assertContains(response, expected_error)
  ```

  * 책 213pg : 에러가 발생하지 않음
  
  ```python
  def test_invalid_list_items_arent_saved(self):
      self.client.post('/list/new', data={'item_text': ''})
      self.assertEqual(List.objects.count(), 0)
      self.assertEqual(Item.objects.count(), 0)
  ```
  
  * 책 221pg : get_absolute_url
    1. 참조 : https://wayhome25.github.io/django/2017/05/05/django-url-reverse/
    2. 모델에 대해서 뷰를 만들게 되면, get_absolute_url() 멤버 함수를 무조건 선언
    3. resolve_url(모델 인스턴스), redirect(모델 인스턴스)를 통해서 모델 인스턴스의 get_abolute_url() 함수를 자동으로 호출
    4. resolve_url 함수는 가장 먼저 get_absolute_url 함수의 존재 여부를 체크하고, 존재할 경우 호출하며 그 리턴값으로 URL을 사용