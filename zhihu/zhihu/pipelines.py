# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy.conf import settings
import pymongo

class ZhihuPipeline(object):
    # def __int__(self):
    #     host = settings["MONGODB_HOST"]
    #     port = settings["MONGODB_PORT"]
    #     dbName = settings["MONGODB_DBNAME"]
    #     client = pymongo.MongoClient(host=host,port=port)
    #     tdb = client[dbName]
    #     self.post = tdb[settings["MONGODB_DBCNAME"]]

    def process_item(self, item, spider):
        settings = spider.settings
        host = settings.get("MONGODB_HOST")
        port = settings.get("MONGODB_PORT")
        dbName = settings.get("MONGODB_DBNAME")
        client = pymongo.MongoClient(host=host,port=port)
        tdb = client[dbName]
        self.post = tdb[settings.get("MONGODB_DBCNAME")]

        zhihu = dict(item)
        self.post.insert(zhihu)

        return item
