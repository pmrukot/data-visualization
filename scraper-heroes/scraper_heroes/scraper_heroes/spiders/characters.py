# -*- coding: utf-8 -*-
import scrapy


class CharactersSpider(scrapy.Spider):
    name = 'characters'
    allowed_domains = ['http://mightandmagic.wikia.com/wiki/Category:Heroes_III_hero_classes']
    start_urls = ['http://http://mightandmagic.wikia.com/wiki/Category:Heroes_III_hero_classes/']

    def parse(self, response):
        pass
