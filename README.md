# Python-tdd-study

![파이썬을 이용한 - 클린코드 위한 테스트 주도 개발](http://image.yes24.com/momo/TopCate471/MidCate001/47009236.jpg) 

해당 책으로 공부할 예정입니다. ~~책 약간 타쿠 느낌이 있습니다.~~ 

## Rule

#### ⏱ 시간

- 매주 수요일 10:00시 (4/22) 시작
- 매주 화요일 23:59 까지 PR 제출



#### ✏ 스터디 방식

- [파이썬을 이용한 - 클린코드 위한 테스트 주도 개발] 책 읽기

- 매주 chap02 ~ chap03 내용을 읽고 정리 후 회고하는 방식으로 진행한다.

- 스터디 관련 온라인 모각코 진행 예정. 참석은 자율! 

- 정리 내용
  - 챕터 정리 (자율)
  - 새로 알게 된 점
  - 같이 이야기 하고 싶은 내용 (셀레니움에 대해, TMI 등 다 됨)
  - 이해가 안가는 내용

- 챕터를 맡은 사람이 그 챕터의 내용을 짧게 설명을 한다. 또한 pr에 다른 팀원이 제출한 내용중 같이 얘기를 해볼 사항 및 어떤 내용이 있었는지 정리를 해서 발표를 한다. 

- 현재 시국으로 인해 google hangout으로 진행. 

- 이후 책 관련 챕터가 끝나면 하나의 프로젝트를 잡고 페어프로그래밍으로 코드를 진행한다.

- 온라인 (vscode liveshare)를 사용해본다. 하지만 효율이 낮다면 오프라인으로 진행한다.

- 페어프로그래밍

  > XP 방법론에서는 개발자가 짝을 이뤄 작업을 하게 된다.  한명이 드라이브 하고 다른 한명이 어떨까? 하고 물으면서 생각을 공유하는 형태로 더 좋은 코드가 나오기 위한 많은 이야기를 하는 시간을 가지면 좋겠습니다.
  >
  > 등에 대해 질문하고 답하는 형식으로 설명한다. 따라서 만약 필자가 잘난 체하는 톤으 로 설명한다면, 필자가 잘나지 못해서 내 자신에게 인내해야 되기 때문이다. 수비적 인 톤으로 말한다면, 귀찮게 하는 사람 역할을 하는 것으로, 어떤 의견이든 논리적으 
  >
  > 로 반대하는 역할을 하는 것이다. 따라서 또 이 수비적 의견을 가진 필자를 확신시키 기 위해 근거 있는 논리를 제시할 것이다. 



##### ⭐️벌금 관련 ⭐️

##### 지각

- 지각은 1,000 원부터
- 이후 피보나치 수열로 오른다
  - 1, 1, 2, 3, 5, ...

##### 결석

- 1번 결석 면제, 이후 5,000원

##### 과제 안할 경우

- 화요일 00:00 시 미제출 경우
  - 1,000원 + 피보나치 (지각 동일)


## Study

### 04/22

- chap01 - 유동관
- chap02 - 강민성
- chap03 - 최지수
- chap04 - 한수민 
- chap05 - 허재

#### 벌금
- 0422 - 수민, 지수 과제 1000

#### 회고

**기능테스트는 UI와 관련이 되어있는가? api에서는 사용이 안되는것인가?**

> 기능테스트란 사용자 관점에서 애플리케이션이 어떻게 동작 하는지 확인할 수 있는 테스트.
> 어떤 흐름을 테스트 하는 거기 때문에 사용할 수 있으나, 보통은 단위 테스트만 테스팅함. 


### 04/29

#### 벌금
- 0429 - 수민, 지수, 동관 과제 1000 

#### 회고 

##### Selenium 셀레늄 기능

> 웹 브라우저의 자동화를 제공해주는 도구. 브라우저 상의 사용자가 상호작용을 하거나, 웹 브라우저에서 상호 교환 가능한 코드를 작성할 수 있도록 지원해준다. 

- ##### find_element_by_

  > 셀리늄 드라이버로 접속한 페이지에서 id , tag, class 등 다양한 값을 가져올 수 있는 함수.

- ##### send_keys

  > 사용자가 enter, ctrl의 특수키 입력이 필요할 경우 전송한다. 
  >
  > `from selenium.webdriver.common.keys import Keys` 가 필요하다.

#### find_element VS find_elements

element는 1개를 찾는데, 값이 없다면 _Exception_ 을 반환한다. 하지만 Elements의 경우 값이 없다면 _Empty list_ 를 반환한다. 

| Find Element                                                 | Find Elements                                                |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| Returns the first most web element if there are multiple web elements found with the same locator | Returns a list of web elements                               |
| Throws exception NoSuchElementException if there are no elements matching the locator strategy | Returns an empty list if there are no web elements matching the locator strategy |
| It will only find one web element                            | It will find a collection of elements whose match the locator strategy. |
| Not Applicable                                               | Each Web element is indexed with a number starting from 0 just like an array |



#### generator expression vs list comprehension

_파이썬을 잘 모르는 사람을 위해 간단히 설명하면, 이 함수들은 Generator Expression 으로 list comprehension 과 비슷하지만 더 진보된 기술이다. 이것에 관한 자료를 찾 아 읽어볼 것을 권한다._

https://stackoverflow.com/questions/47789/generator-expressions-vs-list-comprehension

```python
# Generator expression
(x*2 for x in range(256))

# List comprehension
[x*2 for x in range(256)]
```

*generator expression* 또는 *list expression* 의 결과는 동일한 작업을 수행하는 기능이다. 하지만 메모리 사용의 차이가 있다.

```python
 gen():
    return (something for something in get_some_stuff())
  
print gen()[:2]     # generators don't support indexing or slicing
print [5,6] + gen() # generators can't be added to lists
```

*생성기 표현식* 은 항목에 접근?하므로 매우 한번의 참조는 좋지만, index slicing 또는 다른 가공 작업이 불가능하다. 

이런 차이를 고려해서 두개를 효율적으로 사용할 수 있다.

> stack overflow 의견이 많이 갈리는것으로 보아, 메모리 효율을 고려할것인지, 가공을 많이 하는지에 비례해서 상황에 따라 적용하면 좋을 것 같다. 
>
> 간단히 이해한 내용은 둘다 결과 값은 같으나, yield를 이용해 인덱스를 접근하느냐, 한번에 새로운 목록을 생성해 버리냐의 차이가 있다. 리스트의 경우 같은 목록을 하나 더 생성하므로, 무한대에 가까운 list라면 GE를 쓰는 것을 권장한다.
>
> https://docs.python.org/3/howto/functional.html#generator-expressions-and-list-comprehensions
>
> _This means that list comprehensions aren’t useful if you’re working with iterators that return an infinite stream or a very large amount of data. Generator expressions are preferable in these situations._

##### any()

- Iterator 이 가능한 객체를 받아, 어느 하나의 값이 True 라면 True 값을 반환한다

##### all()

- Iterator 이 가능한 객체를 받아, 모든 값이 True 라면 True 값을 반환한다

#### django

- ##### render()

  HttpResponse 에 감싸져 데이터가 반환된다.

- ##### render_to_string()

  String 형태의 값으로 반환된다.