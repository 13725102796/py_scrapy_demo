# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy_redis.spiders import RedisCrawlSpider
from zhihu.items import ZhihuItem

# 安装redis 通过命令行运行redis-cli 打开多个命令行运行 scrapy crawl userinfo 让其被redis监听
# 在redis中输入网址开始启动分布式爬虫 命令： lpush myspider:start_urls https://www.zhihu.com/api/v4/members/pureri-yue/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20
class UserinfoSpider(RedisCrawlSpider):
    name = 'userInfo'
    redis_key = "myspider:start_urls"
    allowed_domains = ['zhihu.com']
    #start_urls = ['https://www.zhihu.com/api/v4/members/pureri-yue/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20']


    def parse(self, response):
        '''
            name = 用户名
            answer_count = 回答数
            articles_count = 文章数
            url_token = token
            follower_count = 关注数
            headline = 个性签名
            uid = 用户id
            gender = 性别 -1 无 1 男 0 女
            type = 人物
        :param response:
        :return:
        '''

        r = json.loads(response.body)["data"]
        count = len(r)
        if  count < 20:
            pass
        else:
            #继续执行
            page_offset = int(re.findall("&offset=(.*?)&",response.url)[0])
            new_page_offset = page_offset + 20
            next_page_url = response.url.replace("&offset="+ str(page_offset) + "&", "&offset=" + str(new_page_offset) + "&" )
            yield scrapy.Request(url=next_page_url, callback=self.parse)

        for ev_user in r:
            # print(ev_user)
            item = ZhihuItem()
            item["name"] = ev_user["name"]
            item["answer_count"] = ev_user["answer_count"]
            item["articles_count"] = ev_user["articles_count"]
            item["url_token"] = ev_user["url_token"]
            item["follower_count"] = ev_user["follower_count"]
            item["headline"] = ev_user["headline"]
            item["uid"] = ev_user["id"]
            item["gender"] = ev_user["gender"]
            item["type"] = ev_user["type"]
            with open("userinfor.txt","r") as f:
                user_list = f.read()
            if ev_user["url_token"]  not in user_list:
                with open("userinfor.txt","a") as f:
                    f.write(ev_user["url_token"] + "-----")
            yield item

            new_url = "https://www.zhihu.com/api/v4/members/"+ ev_user["url_token"] + "/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20"
            yield scrapy.Request(url = new_url,callback=self.parse)





        # print(r)

        pass
