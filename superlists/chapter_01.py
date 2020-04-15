from selenium import webdriver
browser = webdriver.Chrome("/home/shrldh3576/바탕화면/Gekodriver/chromedriver")
browser.get("http://localhost:8000")

assert "Django" in browser.title



