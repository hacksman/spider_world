# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Aburame.utils import get_config
from Aburame.rules import rules
from Aburame.items import *
from Aburame import urls
from Aburame.loaders import *


class ShinoSpider(CrawlSpider):
    name = 'shino'

    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        start_urls = config.get("start_urls")
        if start_urls:
            if start_urls.get('type') == "static":
                self.start_urls = start_urls.get('value')
            elif start_urls.get('type') == "dynamic":
                self.start_urls = list(eval("urls." + start_urls.get('method'))(*start_urls.get("args", [])))
        self.allowed_domains = config.get('allowed_domains')
        super(ShinoSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls, response=response)

            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == "xpath":
                        loader.add_xpath(key, *extractor.get("args"), **{"re": extractor.get("re")})

            yield loader.load_item()
