from selenium import webdriver

chrome_path = r'/usr/local/bin/chromedriver'
browser = webdriver.Chrome(executable_path=chrome_path)
browser.get('http://localhost:8000')

assert 'Django' in browser.title