# -*- coding: utf-8 -*-

# Scrapy settings for ganji project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'rent'

SPIDER_MODULES = ['rent.spiders']
NEWSPIDER_MODULE = 'rent.spiders'
ITEM_PIPELINES = {
    'rent.pipelines.RentPipeline',
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ganji (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'
LOG_LEVEL = 'INFO'
DOWNLOAD_TIMEOUT = 15