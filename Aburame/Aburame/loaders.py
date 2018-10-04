#!/usr/bin/env python 
# coding:utf-8
# @Time :9/17/18 09:59


from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose, Identity


class ExtractLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # default_output_processor = Identity()


class Dytt8Loader(ExtractLoader):
    download_links_out = Identity()
    contents_out = Compose(Join(), lambda s: s.strip().replace('\n', '').replace('\r', ''))
    pass


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())


class ZcoolInfoLoader(ExtractLoader):
    designer_out = Compose(Join(), lambda s: s.strip().replace('\n', '').replace('\r', ''))
    hometown_out = Compose(Join(), lambda s: s.strip().replace('\n', '').replace('\r', ''))
    introduce_out = Compose(Join(), lambda s: s.strip().replace('\n', '').replace('\r', ''))
    brief_out = Compose(Join("\n"))
    equipment_out = Identity()
    label_out = Identity()
    personal_link_out = Identity()
