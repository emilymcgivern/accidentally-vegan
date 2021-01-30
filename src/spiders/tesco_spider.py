import scrapy

class TescoSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.tesco.ie/groceries/department/default.aspx?N=4294954027&Ne=4294954028' #fresh food
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_content = response.xpath('//li/text()').getall()
        self.log(page_content)