import scrapy
from bs4 import BeautifulSoup

class TescoSpider(scrapy.Spider):
    name = "tesco"

    def start_requests(self):
        urls = [
            'https://www.tesco.ie/groceries/' #fresh food
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        i = 1
        while i < 11:
            results = soup.find(id='nav-' + str(i))
            yield scrapy.Request(url=results.a.get('href'), callback=self.getDepartments)
            i += 1
    
    def getDepartments(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        results = soup.find("div", class_="tertNavContent")
        results2 = results.find_all("a")
        for entry in results2:
            yield scrapy.Request(url=entry.get('href'), callback=self.getItems)

    def getItems(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        results = soup.find("h3", class_="inBasketInfoContainer")
        results2 = results.find_all("a")
        for entry in results2:
            # self.log(entry.find("a"))
            # self.log(entry.get("href"))
            yield scrapy.Request(url='https://www.tesco.ie/' + entry.get('href'), callback=self.getIndividualItemDetails)
    
    def getIndividualItemDetails(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        results = soup.find("div", class_="productDetails")
        # results = soup.find("div", class_="productDetailsContainer")
        itemName = results.find("h1")
        self.log(itemName)
        # soup = BeautifulSoup(response.body, 'html.parser')
        # self.log(soup.find("productDetailsContainer"))
