# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
# import asyncio
import requests
import json

class ProxytestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxytestDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ChangeProxy(object):
    def __init__(self):
        self.get_url= "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=3221f64bf19e446483ca189b74809171&orderno=YZ20191170404yjfymr&returnType=2&count=10"
        self.tem_url = "http://baidu.com"
        self.ip_list = []
        self.count = 0
        self.evecount = 0
        self.useNumber = 1
        # print('-------------1111111111111111111')

    def getIPData(self):
        # if self.useNumber == 0:
        #     pass
        self.useNumber =  self.useNumber -1
        print( '获取ip，并放入ip池=====================================')
        tem_data = requests.get(url=self.get_url).text
        self.ip_list.clear()
        for eve_ip in json.loads(tem_data)["RESULT"]:
            print (eve_ip)
            self.ip_list.append(eve_ip["ip"] + ":" + eve_ip["port"])


    def changeProxy(self,request):
        '''
        修改代理ip
        :param request:
        :return:
        '''
        # request.meta["proxy"] = "http://" + str(self.ip_list[self.count-1]["ip"]) + ":" + str(self.ip_list[self.count-1]["port"])
        request.meta["proxy"] = "http://" + str(self.ip_list[self.count-1])
    def check(self):
        '''
        验证ip
        :return:
        '''
        # requests.get(url=self.temp_url,proxies={"http":str(self.ip_list[self.count-1]["ip"]) + ":" + str(self.ip_list[self.count-1]["port"]) })
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Connection': 'keep-alive'}
        print ("http://" + str(self.ip_list[self.count - 1]) + ", 开始测试")
        r = requests.get(url=self.tem_url,headers=head, proxies={"http":str(self.ip_list[self.count - 1])},timeout=10)
        print ("http://" + str(self.ip_list[self.count-1]) + ", 测试通过" )
        # print(r.text + "==================")

    def ifUsed(self,request):
        try:
            self.changeProxy(request)
            self.check()
        except:
            print("测试不通过======================")
            if self.count == 0 or self.count == 10:
                print("ip池消耗完毕，重新获取中======================")

                self.getIPData()
                # self.getIPData()
                self.count = 1
                self.evecount = 0
            self.count = self.count + 1
            self.ifUsed(request)
        else:
            print("切换下一个ip===============")


    def process_request(self,request,spider):
        # self.getIPData()
        # pass
        #
        if self.count == 0 or self.count == 10:
            self.getIPData()
            self.count = 1
        if self.evecount == 3:
            self.count = self.count + 1
            self.evecount = 0
        else:
            self.evecount = self.evecount + 1
        self.ifUsed(request)

