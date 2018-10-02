# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class WwwDytt8NetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    images = scrapy.Field()
    download_links = scrapy.Field()
    contents = scrapy.Field()
    pass


class NewsItem(scrapy.Item):
    title = scrapy.Field()


class ZcoolItem(scrapy.Item):
    designer = scrapy.Field()
    hot = scrapy.Field()
    score = scrapy.Field()
    fans = scrapy.Field()
    follow = scrapy.Field()


