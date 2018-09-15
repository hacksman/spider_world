#!/usr/bin/env python 
# coding:utf-8
# @Time :9/15/18 15:21

import sys
from scrapy.utils.project import get_project_settings
from www_dytt8_net.spiders.common_spider import CommonSpiderSpider
from www_dytt8_net.utils import get_config
from scrapy.crawler import CrawlerProcess


def run():
    name = sys.argv[1]
    custom_settings = get_config(name)

    spider = custom_settings.get('spider', "common_spider")
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    process = CrawlerProcess(settings)

    process.crawl(spider, **{'name': name})
    process.start()


if __name__ == '__main__':
    run()
