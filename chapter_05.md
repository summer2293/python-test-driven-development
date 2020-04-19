CSRF(cross-site Request Forgery) 공격
``` html
<form>
  {% csrf_token %}
  <input type="text" name="text"/>
  <input type="submit" value="확인"/>
</form>

```
클라이언트에서 해당 페이지를 접속하게 되면 Django 에서 자동으로 csrf_token을 클라이언트로 보내어 cookie에 저장시키고, POST로 전송할 때 cookie의 csrf_token 이 함께 전송되어 인증하는 방식이다
  아래와 같은 공격을 막을 수 있다.

CSRF 공격이란?
CSRF 공격(Cross Site Request Forgery)은 웹 어플리케이션 취약점 중 하나로, 인터넷 사용자(희생자)가 자신의 의지와는 무관하게 공격자가 의도한 행위(수정, 삭제, 등록 등)를 특정 웹사이트에 요청하게 만드는 공격
















