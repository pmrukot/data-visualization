# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector


class ArtistsSpider(scrapy.Spider):
    name = 'artists'
    allowed_domains = ['rateyourmusic.com']

    base_url = 'http://rateyourmusic.com'
    album_chart_url = 'https://rateyourmusic.com/customchart?page={}&chart_type=top&type=album&year=alltime&genre_include=1&include_child_genres=1&genres=&include_child_genres_chk=1&include=both&origin_countries=&limit=none&countries='

    def get_full_url(self, url):
        return self.base_url + url

    def start_requests(self):
        for page in range(1, 2):
            url = self.album_chart_url.format(page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)

        xpath_base = '//*[@id="content"]//span/a[@class="artist"]'

        # artist_names = selector.xpath(xpath_base + '/text()').extract()
        artist_urls = selector.xpath(xpath_base + '/@href').extract()

        for raw_url in artist_urls:
            url = self.get_full_url(raw_url)
            print("#" * 60)
            print(url)
            print("#" * 60)

            yield scrapy.Request(url, callback=self.parse_artist, meta={'url': url})

    def parse_artist(self, response):
        artist_name = response.selector.xpath('//div[@class="artist_name"]/h1/text()').extract()
        print("GOT THE ARTIST DAMMIT {}".format(artist_name))
