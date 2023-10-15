from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

url_list = [
    "https://techcrunch.com/",
    "https://krebsonsecurity.com/",
    "https://thehackernews.com/",
    "https://threatpost.com/",
    "https://www.darkreading.com/",
    "https://www.infosecurity-magazine.com/",
    "https://cyberscoop.com/",
    "https://www.wired.com/category/security/",
    "https://www.securityweek.com/",
    "https://www.csoonline.com/",
    "https://www.ncsc.gov.uk/",
    "https://scholar.google.com/"
]
mentions = []
keyword = "Zero-Trust"

driver = webdriver.Chrome(executable_path=r'C:\Users\samlb\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe')

for url in url_list:

    driver.get(url)
    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    keyword_count = 0

    for tag in soup.find_all(True):
        for attribute, value in tag.attrs.items():
            if keyword.lower() in str(value).lower():
                mentions.append(f"Found keyword '{keyword}' on page {url} in tag {tag.name} and attribute {attribute}: {value}")
                keyword_count += 1
        
        if tag.string:
            if keyword.lower() in tag.string.lower():
                mentions.append(f"Found keyword '{keyword}' on page {url} in tag {tag.name}: {tag.string}")
                keyword_count += 1

    mentions.append(f"Total mentions of keyword '{keyword}' on page {url}: {keyword_count}")
    mentions.append("")

with open(os.getcwd()+'\\zero_trust_findings.txt', 'w') as f:
    f.writelines(mentions)

driver.close()