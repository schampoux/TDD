from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')
print("page title:", browser.title)
assert 'Django' in browser.title 
