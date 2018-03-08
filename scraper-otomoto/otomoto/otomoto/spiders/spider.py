import scrapy


class OtomotoSpider(scrapy.Spider):
    name = "otomoto"

    offers_xpath = '//*[@id="body-container"]//h2[@class="offer-title"]/a/@href'
    price_xpath = '//*[@id="siteWrap"]//span[@class="offer-price__number"]/text()'
    car_params_xpath = '//*[@id="parameters"]/ul[1]/li[span="Kategoria"]/div/a/@title'

    def start_requests(self):
        base_url = 'https://www.otomoto.pl/osobowe/?page='

        for page in range(10000):
            url = base_url + page
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        offers = selector.xpath(self.offers_xpath)
        offers_urls = offers.extract()

        for url in offers_urls:
            yield scrapy.Request(url, callback=self.parse_offer, meta={'url': url})

    def parse_offer(self, response):
        selector = scrapy.Selector(response)
        price = int(selector.xpath(self.price_xpath).extract_first().replace(' ', ''))
        category = selector.xpath(self.car_params_xpath).extract_first()
