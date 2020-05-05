## chap06. 최소 동작 사이트 구축

### 목표
> 기능 테스트 후, database 실행 할 때마다 테스트의 목록이 남아있는데, 다음 테스트의 해석을 방해하는 경우 어떤식으로 해야하나. 


## 요약 

##### LiveServerTestCase

django 에서 제공하는 테스트용 데이터베이스 생성 라이브러리 

## ETC 

### csrf error

Django의 CSRF 보호는 사이트의 각 폼이 생성하는 POST 요청을 확인할 수 있는 토 큰을 자동 생성한다. 지금까지는 순수 HTML로 이루어진 템플릿을 사용했지만, 이제 부터는 Django의 템플릿 마술을 적용하도록 한다. CSRP 토큰을 추가하기 위해 템플 릿 태그를 이용한다.



#### ORM

객체 관계형 맵핑(Object-Relational Mapper, ORM) 

이것을 이용하면 익숙한 객체 지향 코딩 방식을 이용해서 데이터베이스를 처리할 수 있다. 데이터베이스는 클래스로 표현하고, 컬럼은 속성, 레코드는 각 클래스의 인스턴스로 표현한다.



## 새로 알게 된 점



## 같이 이야기 하고 싶은 내용

### 삽질기 

##### url(), path()

> django 에서 request 로 들어온 url 과 view 함수를 맵핑하는 기능.

django 2.0 전에는 url()을 사용했으나 정규표현식을 써야하는 불편함에, 2.0 버전 이후 path()로 사용되었다.

##### url()

```
urlpatterns = [
    url(r'^$', views.BooksModelView.as_view(), name='index'),
    url(r'^book/(?P<pk>\d+)/$', views.BookDetail.as_view(),    name='book_detail')
]
```

##### path()

```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookmark/', BookmarkLV.as_view(), name='index'),
    path('bookmark/<int:pk>/', BookmarkDV.as_view(), name='detail')
]
```

##### _/_ 의 중요성이 존재한다. 놓치지말것...

- name 안붙혀서 error

#### 개고생 error

- url slash

  > error 조건이 201 != 302 로 나서 원인으로 찾기 어려웠다. 주의 할 것 

  ```python
  urlpatterns = [
      path("", views.home_page),
      path("lists/<int:list_id>/", views.view_list, name="view_list"),
      path("lists/new", views.new_list, name="new_list"),
      path("lists/<int:list_id>/add_item", views.add_item, name="add_item"),
  ]
  ```

  views

  ```python
  def new_list(request):
      list_ = List.objects.create()
      Item.objects.create(text=request.POST["item_text"], list=list_)
      # return redirect(f"/lists/{list_.id}")
      return redirect(f"/lists/{list_.id}/")
  
  
  def add_item(request, list_id):
      list_ = List.objects.get(id=list_id)
      Item.objects.create(text=request.POST["item_text"], list=list_)
      # return redirect(f"/lists/{list_.id}")
      return redirect(f"/lists/{list_.id}/")
  
  ```

  



## 이해가 안가는 내용





## 참조 사이트 
> https://laravel.com/docs/7.x/csrf
> https://docs.djangoproject.com/en/dev/ref/csrf/#testing
>
> [https://medium.com/@lyoungh2570/django-url%EA%B3%BC-path-f75ec1754460](https://medium.com/@lyoungh2570/django-url과-path-f75ec1754460)

