# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import io
reload(sys)
sys.setdefaultencoding('utf8')
# '''
#        h1 = 大标题
#        title = 电影名字
#        img = 电影图片
#        score = 电影评分
#        url = 电影链接
#        :param response:
#        :return:
# '''
import os
pathdir = os.getcwd()

class MoviePipeline(object):
    def process_item(self, item, spider):
        year = spider.settings.get('YEAR')[0]
        filename = pathdir + '\\data\\movie' + year + '.txt'
        print(year)
        with io.open(filename,'a',encoding='utf8') as f:
            f.write('h1:' + item['h1'] + '\n'+'________________________________________')
            for i in range(10):
                scoreStr = str(item['score'][i])
                f.write('电影名字:' + item['title'][i]+ '\n')
                f.write('电影图片:' + item['img'][i] + '\n')
                f.write(u'电影评分:'+ scoreStr + '\n')
                f.write('电影链接:' + item['url'][i] + '\n' + '------------------------' + '\n')


        return item
