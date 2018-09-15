#!/usr/bin/env python 
# coding:utf-8
# @Time :9/15/18 10:33

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose

class ExtractLoader(ItemLoader):
    default_output_processor = TakeFirst()


class Dytt8Loader(ExtractLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())