#!/usr/bin/env python 
# coding:utf-8
# @Time :9/17/18 09:58

from scrapy.linkextractors import LinkExtractor
from scrapy.spider import Rule

rules = {
    "dytt8":
        (
            # 追踪除游戏外的所有列表页
            Rule(LinkExtractor(deny=r'.*game.*', allow='.*/index\.html')),
            # 对下一页进行追踪
            Rule(LinkExtractor(restrict_xpaths=u'//a[text()="下一页"]')),
            # 对文章进行提取并回调给parse_item处理, 过滤掉游戏
            Rule(LinkExtractor(allow=r'.*/\d+/\d+\.html', deny=r".*game.*"), callback='parse_item', follow=True),
        ),

    'china': (
        Rule(LinkExtractor(allow='article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
    ),

    'zcool': (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="laypage_next"]')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="visitor-name"]')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="card-img-hover"]')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="usernick"]')),
        Rule(LinkExtractor(allow='.*www.zcool.com.cn\/u\/\d+$')),
        # Rule(LinkExtractor(restrict_xpaths='//a[@class="visitor-name"]')),
        # Rule(LinkExtractor(restrict_xpaths='//a[@class="userimg"]')),
        # Rule(LinkExtractor(allow='//a[@class="userHome_tab_profile"]'), callback='parse_item'),
        # Rule(LinkExtractor(allow='.*?profile#tab_anchor$'), callback='parse_item'),
        Rule(LinkExtractor(allow='.*?profile.*'), callback='parse_item'),
        # Rule(LinkExtractor(restrict_xpaths='//a[@class="userHome_tab_profile"]'), callback='parse_item'),
        # Rule(LinkExtractor(allow='.*www.zcool.com.cn.*?profile#tab_anchor$'), callback='parse_item')
    )
    # https://xuyiyun.zcool.com.cn
}