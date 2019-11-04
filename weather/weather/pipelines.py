# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import io
import json
import pymongo
import pymysql
pathdir = os.getcwd()
print pathdir


# 储存到mysql
class W2mysql(object):

    def process_item(self,item,spider):
        print '-------------------2222222222222222'
        # print('\n'.join(['%s:%s' % item for item in spider.settings.__dict__.items()]))
        print(spider.settings)
        print (spider.settings.get('CITY'))
        print '-------------------2222222222222222'
        connection = pymysql.connect(host="localhost",user="root",password="188208",charset="utf8mb4")
        curs = connection.cursor()
        # create database 数据库
        try:
            curs.execute('create database weather_test')
        except:
            print 'WEATHER_TEST is exists'

        connection.select_db('weather_test')
        # create 表
        try:
            curs.execute('create table weathers(id int(11) KEY NOT NULL AUTO_INCREMENT)')
        except Exception as e:
            #connection.rollback()
            print e
            print('weathers is exists')

        # # create 字段
        # try:
        #     for i in range(4):
        #         sql = "alter table weather add key%s varchar(64) not null" %i
        #         curs.execute(sql)
        # except Exception, e:
        #     print e
        #
        # # insert 插入数据
        # for i in range(4):
        #     sql = "insert into weather set id=%s" %i
        #     curs.execute(sql)
        #     sql = "update weather set name = 'hello%s' where id= %s"%(i,i)
        #     curs.execute(sql)
        #     for j in range(4):
        #         sql = "update weather set key%s='world%s%s' where id=%s"%(j,i,j,i)
        #         curs.execute(sql)

        try:
            attr = ['data','week','high_temperature','low_temperature','weather','wind','img']
            for i in attr:
                sql = "alter table weathers add %s text not null" %i
                curs.execute(sql)
        except Exception, e:
            print e
        print item
        try:
            with curs as cursor:
                sql = "insert into `weathers`(`data`,`week`,`high_temperature`,`low_temperature`,`weather`,`wind`,`img`)values(%s,%s,%s,%s,%s,%s,%s)"
                for i in range(7):
                    cursor.execute(sql, (
                        item['data'][i], item['week'][i], item['high_temperature'][i], item['low_temperature'][i],
                        item['weather'][i],
                        item['wind'][i], item['img'][i]))

        finally:
            connection.commit()
            curs.close()
            connection.close()
        return item


# 储存到txt
class WeatherPipeline(object):
    def process_item(self, item, spider):
        filename = pathdir + '\\data\\weather.txt'
        # print item
        with io.open(filename, 'a+', encoding='utf8') as f:
            for i in range(7):
                f.write('日期:' + item['data'][i] + '\n')
                f.write('星期:' + item['week'][i] + '\n')
                f.write('最高温度:' + item['high_temperature'][i] + '\n')
                f.write('最低温度:' + item['low_temperature'][i] + '\n')
                f.write('天气:' + item['weather'][i] + '\n')
                f.write('风况:' + item['wind'][i] + '\n' + '--------------------------------' + '\n')
                # f.write('\n')
        return item

# 储存到 json
class W2json (object):
    def process_item(selfself,item,spider):
        filename = pathdir + '\\data\\weather.json'

        with io.open(filename,'a+',encoding="utf8") as f:
            line = json.dumps(dict(item),ensure_ascii=False) + '\n'
            f.write(line)

        return item


# 储存到 mongoDB
class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()







