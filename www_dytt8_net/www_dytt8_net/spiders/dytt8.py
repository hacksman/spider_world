# -*- coding: utf-8 -*-
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from www_dytt8_net.loaders import Dytt8Loader
from www_dytt8_net.items import WwwDytt8NetItem


class Dytt8Spider(CrawlSpider):

    __ERROR_INFO = "很抱歉，您要访问的页面已被删除或不存在。"

    name = 'dytt8'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['http://www.dytt8.net/']

    rules = (
        # 追踪除游戏外的所有列表页
        Rule(LinkExtractor(deny=r'.*game.*', allow='.*/index\.html')),
        # 对下一页进行追踪
        Rule(LinkExtractor(restrict_xpaths=u'//a[text()="下一页"]')),
        # 对文章进行提取并回调给parse_item处理, 过滤掉游戏
        Rule(LinkExtractor(allow=r'.*/\d+/\d+\.html', deny=r".*game.*"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if self.__ERROR_INFO in response.text:
            return
        loader = Dytt8Loader(item=WwwDytt8NetItem(), response=response)
        loader.add_xpath("title", '//div[@class="title_all"]/h1/font/text()')
        loader.add_xpath('publish_time', '//div[@class="co_content8"]/ul/text()', re='发布时间：(\d{4}-\d{2}-\d{2})')
        loader.add_xpath('images', '//div[@id="Zoom"]//img//@src')
        loader.add_xpath('download_links', '*', re='<a href="(ftp://.*?)">')
        loader.add_xpath("contents", 'string(//div[@id="Zoom"])')
        yield loader.load_item()

