#!/usr/bin/env python 
# coding:utf-8
# @Time :9/15/18 10:33

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose, Identity

class ExtractLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # default_output_processor = Identity()

class Dytt8Loader(ExtractLoader):
    download_links_out = Identity()
    contents_out = Compose(Join(), lambda s: s.strip().replace('\n', '').replace('\r', ''))
    pass