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
        # 追踪下一页
        Rule(LinkExtractor(restrict_xpaths='//a[@class="laypage_next"]')),
        # 提取如 https://www.zcool.com.cn/u/15472001 样式的页面
        Rule(LinkExtractor(allow='.*www.zcool.com.cn\/u\/\d+$')),
        # 追踪 https://www.zcool.com.cn/designer 页面设计师主页的链接
        Rule(LinkExtractor(restrict_xpaths='//a[@z-st="user_content_card_1_user_name"]')),
        # 追踪 https://www.zcool.com.cn/designer 筛选 | 推荐设计师 栏目的分页
        Rule(LinkExtractor(restrict_xpaths='//a[starts-with(@z-st, "desinger_filter_recommend")]')),
        # 追踪 https://www.zcool.com.cn/designer 筛选 | 不限职业 栏目的分页
        Rule(LinkExtractor(restrict_xpaths='//a[starts-with(@z-st, "desinger_filter_profession")]')),
        # 本来准备使用访客和留言来追踪的，后来发现页面是动态加载的，提取收到该信息，遂弃用
        # Rule(LinkExtractor(restrict_xpaths='//a[@class="usernick"]')),
        # Rule(LinkExtractor(restrict_xpaths='//a[@class="visitor-name"]')),
        # 追踪 粉丝页面
        Rule(LinkExtractor(allow='.*?fans.*')),
        # 追踪 关注页面
        Rule(LinkExtractor(allow='.*?follow.*')),
        # 追踪 设计师资料页，并回调给parse_item函数处理
        Rule(LinkExtractor(allow='.*?profile.*'), callback='parse_item'),
    )
}
