# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem


class BeijingspiderSpider(scrapy.Spider):
    name = 'Beijing'
    citys = ['chongqing','yanhuqu','beijing']
    custom_settings = {
        'CITY': citys
    }
    allowed_domains = ['tianqi.com']
    #start_urls = ['http://www.tianqi.com/beijing/']

    start_urls = []
    for city in citys:
        start_urls.append('http://wwww.tianqi.com/' + city + '/')
    def parse(self, response):
        '''
        date = 当日日期
        week = 星期几
        img = 当日天气图标
        wind = 当日风况
        weather = 当日天气
        high_temperature = 当日最高温度
        low_temperature = 当日最低温度
        :param response:
        :return:
        '''
        print '11111111111111111111111111111111--------------------'
        print (self.settings.get('CITY'))
        print("URL: " + response.request.url)
        print '11111111111111111111111111111111--------------------'


        # oneweek = response.xpath('//div[@class="day7"]')
        item = WeatherItem()
        data = response.xpath('//div[@class="day7"]//ul[@class="week"]//li//b/text()').extract()
        week = response.xpath('//div[@class="day7"]//ul[@class="week"]//li//span/text()').extract()
        base_url = 'http:'
        img = response.xpath('//div[@class="day7"]//ul[@class="week"]//li//img/@src').extract()
        imgs = []
        for i in range(7):
            img_i = img[i]
            img_url = base_url + img_i
            imgs.append(img_url)
        # print(data)
        # print(week)
        # print(imgs)
        weather = response.xpath('//div[@class="day7"]//ul[@class="txt"]//li/text()').extract()
        high_temperature = response.xpath('//div[@class="day7"]//div[@class="zxt_shuju"]//ul//li//span/text()').extract()
        low_temperature = response.xpath('//div[@class="day7"]//div[@class="zxt_shuju"]//ul//li//b/text()').extract()
        # print(high_temperature)
        # print(low_temperature)
        wind = response.xpath('//div[@class="day7"]//ul[@class="txt"]//li/text()').extract()
        # print(wind)

        item['data'] = data
        item['week'] = week
        item['img'] = imgs
        item['weather'] = weather
        item['wind'] = wind
        item['high_temperature'] = high_temperature
        item['low_temperature'] = low_temperature
        yield item
