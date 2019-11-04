# -*- coding: utf-8 -*-

import scrapy
import json
from movie.items import MovieItem

class MovieSpider(scrapy.Spider):
    name = 'MovieSpider'
    allowed_domains = ['douban.com']
    start_urls = []
    # https://movie.douban.com/ithil_j/activity/movie_annual2017/widget/1
    #
    years = ['2015']
    custom_settings = {
        'YEAR': years
    }

    for year in years:
        for j in range(50):
            start_urls.append('https://movie.douban.com/ithil_j/activity/movie_annual' + year + '/widget/' + str(j) )
    def parse(self, response):
        '''
        h1 = 大标题
        title = 电影名字
        img = 电影图片
        score = 电影评分
        url = 电影链接
        :param response:
        :return:
        '''
        item = MovieItem()
        # h1 = response.xpath('//div[@class="Rz9z5"]//h1//div/text()').extract()
        # title = response.xpath('//div[@class="_2mn2i"]//h2//a/text()').extract()
        # img = response.xpath('//div[@class="_4Bt8x"]//div[@class="_-9ptq"]//a/@style').extract()
        # score = response.xpath('//div[@class="_3uGjJ"]//div[@class="_2d6nY"]//div[@class="_2YEJY"]/text()').extract()
        # url = response.xpath('//div[@class="_2mn2i"]//h2//a/@href').extract()
        jsobj = json.loads(response.body)
        subject = jsobj['res']['subjects']
        if subject:
            item['h1'] = jsobj['res']['payload']['title']
            title = []
            img = []
            score = []
            url = []
            for sub in subject:
                title.append(sub['title'])
                img.append(sub['cover'])
                score.append(sub['rating'])
                url.append(sub['url'])

            item['title'] = title
            item['img'] = img
            item['score'] = score
            item['url'] = url
        else:
            item = []
        yield item


