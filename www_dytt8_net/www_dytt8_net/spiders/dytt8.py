# -*- coding: utf-8 -*-
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import Compose
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
        item = WwwDytt8NetItem()
        item['title'] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract_first()
        item['publish_time'] = response.xpath('//div[@class="co_content8"]/ul/text()').extract_first().strip().replace('发布时间：', '')
        imgs_xpath = response.xpath('//div[@id="Zoom"]//img')
        item['images'] = [i.xpath('./@src').extract_first() for i in imgs_xpath if i.xpath('./@src')]
        item['download_links'] = re.compile('<a href="(ftp://.*?)">').findall(response.text)
        item['contents'] = [i.strip().replace('\n', '').replace('\r', '') for i in response.xpath('string(//div[@id="Zoom"])').extract()]
        yield item
