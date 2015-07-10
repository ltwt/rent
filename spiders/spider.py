# -*- coding:utf-8 -*-
__author__ = 'wt'
import re
import uuid
import json

from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from rent.items import *
from rent.misc.log import *
import sys


class Spider(Spider):
    reload(sys)
    name="gjrent"
    allowed_domains=["ganji.com"]
    start_urls = []
    for i in range(1,100,1):
        url="http://nj.ganji.com/fang2/o"+bytes(i)+"/"
        print url
        start_urls.append(url)
    count=0
    def parse(self, response):
        print response
        hxs=HtmlXPathSelector(response)
        items=[]
        urls= hxs.select('//a/@href').extract()
        for url in urls:
            if "fang2" in url and "htm" in url:
                items.append(Request("http://nj.ganji.com"+url,callback=self.parse_rent))
        return items

    def parse_rent(self,response):
        item=RentItem()
        sel=Selector(response)
        #主键
        item['guid']=uuid.uuid1()
        #标题
        siteTitle=sel.xpath('//div[@class="col-cont title-box"]/h1/text()').extract()
        item['title']=re.sub("\s*","",siteTitle[0])
        #主要内容
        sites=sel.xpath('//div[@class="leftBox"]/div/div/div/ul/li').extract()
        for  site in sites:
            matchObj =re.search("class=\"fc-gray\">.*"+'：'.decode('utf8'),site,0)
            if matchObj:
                type=matchObj.group().replace("class=\"fc-gray\">","").replace('：'.decode('utf8'),"")
                #期望租金
                if type== '期望租金'.decode('utf8'):
                    qwzjSite=Selector(text=site).xpath('.//text()').extract()
                    #正则表达式去掉空
                    item['qwzj']=re.sub("\s*","",qwzjSite[1])
                #期望户型
                elif type== '期望户型'.decode('utf8'):
                    qwhxSite=Selector(text=site).xpath('.//text()').extract()
                    item['qwhx']=re.sub("\s*","",qwhxSite[1])
                #期望小区
                elif type== '期望小区'.decode('utf8'):
                    qwxqSite=Selector(text=site).xpath('.//text()').extract()
                    if len(qwxqSite)>2:
                        item['qwxq']=re.sub("\s*","",qwxqSite[2])
                    elif len(qwxqSite)>1:
                        item['qwxq']=re.sub("\s*","",qwxqSite[1])
                #期望区域
                elif type== '期望区域'.decode('utf8'):
                    sitesQWQY=Selector(text=site).xpath('.//a').extract()
                    qwqy=''
                    for i in range(0,len(sitesQWQY)-1,1):
                        str=re.search(">.*</a",sitesQWQY[i],0)
                        qwqy+=str.group().replace(">","").replace("</a","")+'-'
                        #去掉最后一个字符
                    item['qwqy']=qwqy[0:-1]
                #期望地点
                elif type== '期望地点'.decode('utf8'):
                    qwddSite=Selector(text=site).xpath('.//text()').extract()
                    item['qwdd']=re.sub("\s*","",qwddSite[2])
                else:
                    pass
        #联系方式
        sitesContact=sel.xpath('//div[@class="basic-info-contact"]/div').extract()
        if sitesContact:
            #联系人及身份
            contactPerson=sitesContact[0]
            sitesPerson= Selector(text=contactPerson).xpath('.//i').extract()
            lxrSite=Selector(text=sitesPerson[0]).xpath('.//text()').extract()
            item['lxr']=re.sub("\s*","",lxrSite[0])
            lxrsfSite=Selector(text=sitesPerson[1]).xpath('.//text()').extract()
            item['lxrsf']=re.sub("\s*","",lxrsfSite[0])
            #联系电话
            contactTelphone=sitesContact[1]
            sitsTelphone=Selector(text=contactTelphone).xpath('.//em').extract()
            siteLXFS=Selector(text=sitsTelphone[0]).xpath('.//text()').extract()
            item['lxfs']=re.sub("\s*","",siteLXFS[0])
        #备注
        bzSite=sel.xpath('//div[@class="summary-cont"]/text()').extract()
        strBz=''
        for i in range(0,len(bzSite)-1,1):
            strBz+=bzSite[i]
        item['bz']=re.sub("\s*","",strBz)
        return item



