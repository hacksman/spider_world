#!/usr/bin/env python 
# coding:utf-8
# @Time :9/17/18 10:28

import random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RandomUserAgentMiddleware(UserAgentMiddleware):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, settings, user_agent='Scrapy'):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent
        user_agent_file = settings.get('USER_AGENT_LIST')
        if not user_agent_file:
            ua = settings.get('USER_AGENT', user_agent)
            self.user_agent_list = [ua]
        else:
            with open(user_agent_file, 'r') as f:
                self.user_agent_list = [i.strip() for i in f.readlines()]

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', user_agent)
