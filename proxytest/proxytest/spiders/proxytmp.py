# -*- coding: utf-8 -*-
import scrapy


class ProxytmpSpider(scrapy.Spider):
    name = 'proxytmp'
    allowed_domains = ["baidu.com"]
    start_urls = ["http://baidu.com",]
    def parse(self, response):
        mimvp_url = response.url  # 爬取时请求的url
        body = response.body  # 返回网页内容

        print("mimvp_url : " + str(mimvp_url) + "开始爬取内容===================")

        # print("body : " + str(body))
        yield
        pass
