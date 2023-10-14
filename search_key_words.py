from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = "https://students.carleton.ca/"
keyword = "community"

driver = webdriver.Chrome(executable_path=r'C:\Users\samlb\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe')
driver.get(url)
time.sleep(5)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
keyword_count = 0

for tag in soup.find_all(True):
    for attribute, value in tag.attrs.items():
        if keyword.lower() in str(value).lower():
            print(f"Found keyword '{keyword}' on page {url} in tag {tag.name} and attribute {attribute}: {value}")
            keyword_count += 1
    
    if tag.string:
        if keyword.lower() in tag.string.lower():
            print(f"Found keyword '{keyword}' on page {url} in tag {tag.name}: {tag.string}")
            keyword_count += 1

print(f"Total mentions of keyword '{keyword}' on page {url}: {keyword_count}")
driver.close()
 