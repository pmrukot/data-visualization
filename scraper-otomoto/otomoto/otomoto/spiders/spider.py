import scrapy


class OtomotoSpider(scrapy.Spider):
    name = "otomoto"

    offers_xpath = '//*[@id="body-container"]//h2[@class="offer-title"]/a/@href'
    price_xpath = '//*[@id="siteWrap"]//span[@class="offer-price__number"]/text()'
    car_params_xpath_link = '//*[@id="parameters"]/ul[1]/li[span="{}"]/div/a/@title'
    car_params_xpath = '//*[@id="parameters"]/ul[1]/li[span="{}"]/div/text()'

    def get_selector_for_category(self, selector, category, islink=True):
        xpath = self.car_params_xpath_link if islink else self.car_params_xpath
        return selector.xpath(xpath.format(category))

    def postprocess(self, data):
        data = data.extract_first()
        return data.replace('\n', '').replace('  ', '') if data else None

    def start_requests(self):
        base_url = 'https://www.otomoto.pl/osobowe/?page='

        for page in range(10000):
            url = base_url + str(page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        offers = selector.xpath(self.offers_xpath)
        offers_urls = offers.extract()

        for url in offers_urls:
            yield scrapy.Request(url, callback=self.parse_offer, meta={'url': url})

    def parse_offer(self, response):
        selector = scrapy.Selector(response)
        price = selector.xpath(self.price_xpath)
        offer_from = self.get_selector_for_category(selector, 'Oferta od')
        category = self.get_selector_for_category(selector, 'Kategoria')
        brand = self.get_selector_for_category(selector, 'Marka pojazdu')
        label = self.get_selector_for_category(selector, 'Model pojazdu')
        version = self.get_selector_for_category(selector, 'Wersja')
        production_year = self.get_selector_for_category(selector, 'Rok produkcji', islink=False)
        mileage = self.get_selector_for_category(selector, 'Przebieg', islink=False)
        displacement_capacity = self.get_selector_for_category(selector, 'Pojemność skokowa', islink=False)
        vin = self.get_selector_for_category(selector, 'VIN', islink=False)
        power = self.get_selector_for_category(selector, 'Moc', islink=False)
        fuel_type = self.get_selector_for_category(selector, 'Rodzaj paliwa')
        transmission = self.get_selector_for_category(selector, 'Skrzynia biegów')
        drive = self.get_selector_for_category(selector, 'Napęd')
        particulate_filter = self.get_selector_for_category(selector, 'Filtr cząstek stałych', islink=False)
        type = self.get_selector_for_category(selector, 'Typ')
        doors_number = self.get_selector_for_category(selector, 'Liczba drzwi', islink=False)
        seats_number = self.get_selector_for_category(selector, 'Liczba miejsc', islink=False)
        color = self.get_selector_for_category(selector, 'Kolor')
        metallic = self.get_selector_for_category(selector, 'Metalik', islink=False)
        financing_possibility = self.get_selector_for_category(selector, 'Możliwość finansowania', islink=False)
        vat_invoice = self.get_selector_for_category(selector, 'Faktura VAT', islink=False)
        accidents = self.get_selector_for_category(selector, 'Bezwypadkowy')
        state = self.get_selector_for_category(selector, 'Stan')

        yield {
            'price': int(price.extract_first().replace('\n', '').replace(' ', '')),
            'offer_from': self.postprocess(offer_from),
            'category': self.postprocess(category),
            'brand': self.postprocess(brand),
            'label': self.postprocess(label),
            'version': self.postprocess(version),
            'production_year': self.postprocess(production_year),
            'mileage': self.postprocess(mileage),
            'displacement_capacity': self.postprocess(displacement_capacity),
            'vin': self.postprocess(vin),
            'power': self.postprocess(power),
            'fuel_type': self.postprocess(fuel_type),
            'transmission': self.postprocess(transmission),
            'drive': self.postprocess(drive),
            'particulate_filter': self.postprocess(particulate_filter),
            'type': self.postprocess(type),
            'doors_number': self.postprocess(doors_number),
            'seats_number': self.postprocess(seats_number),
            'color': self.postprocess(color),
            'metallic': self.postprocess(metallic),
            'financing_possibility': self.postprocess(financing_possibility),
            'vat_invoice': self.postprocess(vat_invoice),
            'accidents': self.postprocess(accidents),
            'state': self.postprocess(state),
        }
