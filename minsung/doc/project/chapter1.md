# [chapter01] '행복' 프로젝트 Authentication

### 기본 데이터 생성

``` python
self.email = 'rkdalstjd9@naver.com'
self.password = "qwe123"
self.valid_profile = {
    "profile": {
        "email": self.email,
        "password": self.password
    }
}
```

> 해당 패스워드는 테스트 용도로 바꾼 것이니 눈독들이지 마세요!



### 유저 생성 테스트

``` python
def test_create_valid_profile(self):
    client = Client()
    response = client.post(
        reverse('signup'),
        data=json.dumps(self.valid_profile),
        content_type='application/json'
    )
    self.assertEqual(
        response.data['response'], 'success'
    )
```

> valid한 데이터에 대해서 테스트를 하면 invalid한 데이터에서도 테스트를 해야하나?
>
> 그렇다면 어디까지 해야하나





### 유저 인증 테스트

인증되지 않은 사용자에 대한 로그인

``` python
def test_login_without_email_active(self):
    profile = self.create_user()
    client = Client()
    response = client.post(
        reverse('login'),
        data=json.dumps({
            "email": profile.email,
            "password": self.password
        }),
        content_type='application/json'
  )

  self.assertEqual(
      response.data,
      {
          "non_field_errors": [
              "Unable to log in with provided credentials."
          ]
      }
  )
```

> response에 대해서 status_code 검사? data검사? 무엇을 해야하는가
> 한다면 다음과 같이 정적으로 하는게 맞는가



인증된 사용자에 대한 로그인

``` python
def test_login_with_email_active(self):
    profile = self.create_user()
    profile.status = '1'
    profile.save()

    client = APIClient()
    response = client.post(
        reverse('login'),
        data=json.dumps({
            "email": "rkdalstjd9@naver.com",
            "password": "qwe123"
            # "email": profile.email,
            # "password": self.password
        }),
        content_type='application/json'
    )
    self.assertEqual(
        response.status_code,
        200
    )
```

> 계속 에러가 난다. 아직 해결을 못함



### 전체 코드

```python
from django.test import TestCase, Client
from rest_framework.test import APIClient
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest import skip


class CreateProfileTest(TestCase):

    def setUp(self):
        self.email = 'rkdalstjd9@naver.com'
        self.password = "qwe123"
        self.valid_profile = {
            "profile": {
                "email": self.email,
                "password": self.password
            }
        }

    @skip
    def test_create_valid_profile(self):
        client = Client()
        response = client.post(
            reverse('signup'),
            data=json.dumps(self.valid_profile),
            content_type='application/json'
        )
        self.assertEqual(
            response.data['response'], 'success'
        )

    def create_user(self):
        User = get_user_model()
        email = self.email
        password = self.password
        profile = User(
            email=email,
            password=password
        )
        profile.status = '0'
        profile.role = '0'
        profile.save()
        return profile

    @skip
    def test_login_without_email_active(self):
        profile = self.create_user()
        client = Client()
        response = client.post(
            reverse('login'),
            data=json.dumps({
                "email": profile.email,
                "password": self.password
            }),
            content_type='application/json'
        )

        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "Unable to log in with provided credentials."
                ]
            }
        )

    def test_login_with_email_active(self):
        profile = self.create_user()
        profile.status = '1'
        profile.save()

        client = APIClient()
        response = client.post(
            reverse('login'),
            data=json.dumps({
                "email": "rkdalstjd9@naver.com",
                "password": "qwe123"
                # "email": profile.email,
                # "password": self.password
            }),
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            200
        )

```

