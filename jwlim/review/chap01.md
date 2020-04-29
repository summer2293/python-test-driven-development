### Chap01 : 기능 테스트를 이용한 Django 설치


* 책에서는 Firefox를 사용한 예제였지만, Chrome을 이용해서 진행함.  
* `brew cask install chromedriver`  
```
from selenium import webdriver  

chrome_path = r'/usr/local/bin/chromedriver'  
browser = webdriver.Chrome(executable_path=chrome_path)  
browser.get('http://localhost:8000')  

assert 'Django' in browser.title  
```  