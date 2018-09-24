#!/usr/bin/env python 
# coding:utf-8
# @Time :9/17/18 10:02

import sys
from scrapy.utils.project import get_project_settings
from Aburame.spiders.shino import ShinoSpider
from Aburame.utils import get_config
from scrapy.crawler import CrawlerProcess


def run():
    name = sys.argv[1]
    custom_settings = get_config(name)

    spider = custom_settings.get('spider', "shino")
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    process = CrawlerProcess(settings)

    process.crawl(spider, **{'name': name})
    process.start()


if __name__ == '__main__':
    run()
