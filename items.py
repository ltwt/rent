# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class RentItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field(default='')
    qwzj = Field(default='')
    qwhx = Field(default='')
    qwxq = Field(default='')
    qwqy = Field(default='')
    qwdd = Field(default='')
    lxr = Field(default='')
    lxrsf =Field(default='')
    lxfs = Field(default='')
    bz = Field(default='')
    guid=Field(default='')
    pass
