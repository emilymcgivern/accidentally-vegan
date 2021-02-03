import re
import scrapy
from bs4 import BeautifulSoup

class TescoSpider(scrapy.Spider):
    name = "tesco"

    def start_requests(self):
        urls = [
            'https://www.tesco.ie/groceries' #fresh food
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        i = 1
        while i < 6:
            results = soup.find(id='nav-' + str(i))
            yield scrapy.Request(url=results.a.get('href'), callback=self.getDepartments)
            i += 1
    
    def getDepartments(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        results = soup.find("div", class_="tertNavContent")
        departmentUrl = results.find_all("a")
        for entry in departmentUrl:
            yield scrapy.Request(url=entry.get('href'), callback=self.getItems)

    def getItems(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        results = soup.find("h3", class_="inBasketInfoContainer")
        itemUrl = results.find_all("a")
        for entry in itemUrl:
            yield scrapy.Request(url='https://www.tesco.ie/' + entry.get('href'), callback=self.getIndividualItemDetails)
    
    def getIndividualItemDetails(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        results = soup.find("div", class_="detailsBox")
        isVegan = results.find_all(text=re.compile("Suitable for Vegans"))
        if (len(isVegan) > 0):
            itemHeader = soup.find("div", class_="productDetails")
            itemName = itemHeader.find("h1")
            with open('vegan.txt', 'a') as f:
                f.write(itemName.text + ' ' + response.url + '\n')
