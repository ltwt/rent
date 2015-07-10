# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class RentPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
        host='localhost',
        db = 'ugc',
        user = 'root',
        passwd = '1234',
        cursorclass = MySQLdb.cursors.DictCursor,
        charset = 'utf8',
        use_unicode = False
        )


    def process_item(self, item, spider):
        item.setdefault('title','')
        item.setdefault('qwzj','')
        item.setdefault('qwhx','')
        item.setdefault('qwxq','')
        item.setdefault('qwqy','')
        item.setdefault('qwdd','')
        item.setdefault('lxr','')
        item.setdefault('lxrsf','')
        item.setdefault('lxfs','')
        item.setdefault('bz','')
        item.setdefault('guid','')
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    #将每条数据写入数据库中
    def _conditional_insert(self, tx, item):
            tx.execute("insert into rent(title,qwzj,qwhx,qwxq,qwqy,qwdd,lxr,lxrsf,lxfs,bz,guid) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" ,(item['title'],item['qwzj'],item['qwhx'],item['qwxq'],item['qwqy'],item['qwdd'],item['lxr'],item['lxrsf'],item['lxfs'],item['bz'],item['guid']))


