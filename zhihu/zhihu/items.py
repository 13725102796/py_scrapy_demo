# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    url_token = scrapy.Field()
    follower_count = scrapy.Field()
    headline = scrapy.Field()
    uid = scrapy.Field()
    gender = scrapy.Field()
    type = scrapy.Field()

    pass