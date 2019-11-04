# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'movie'
    h1 = scrapy.Field()
    title = scrapy.Field()
    img = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field()
    pass
