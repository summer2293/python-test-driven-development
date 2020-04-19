CSRF(cross-site Request Forgery) 공격
``` html

<form>
  {% csrf_token %}
  <input type="text" name="text"/>
  <input type="submit" value="확인"/>
</form>

```















