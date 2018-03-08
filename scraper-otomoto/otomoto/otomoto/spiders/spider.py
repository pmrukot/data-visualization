import scrapy


class OtomotoSpider(scrapy.Spider):
    name = "otomoto"

    def start_requests(self):
        base_url = 'https://www.otomoto.pl/osobowe/?page='

        for page in range(10000):
            url = base_url + page
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)


    def parse_offer(self, response):
        pass
