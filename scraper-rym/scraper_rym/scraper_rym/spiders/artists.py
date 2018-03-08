# -*- coding: utf-8 -*-
import scrapy


class ArtistsSpider(scrapy.Spider):
    name = 'artists'
    allowed_domains = ['rateyourmusic.com']
    start_urls = ['http://rateyourmusic.com/']

    def parse(self, response):
        pass
