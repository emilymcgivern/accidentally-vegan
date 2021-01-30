import requests
from bs4 import BeautifulSoup

URL = 'https://www.tesco.ie/groceries/'
page = requests.get(URL)
page_content = BeautifulSoup(page.content, 'html.parser')

print (page_content)