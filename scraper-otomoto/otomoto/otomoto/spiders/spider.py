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
        offers = selector.xpath('//*[@id="body-container"]//h2[@class="offer-title"]/a/@href')
        offers_urls = offers.extract()

        for url in offers_urls:
            yield scrapy.Request(url, callback=self.parse_offer, meta={'url': url})

    def parse_offer(self, response):
        pass
