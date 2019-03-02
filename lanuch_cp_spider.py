#!/usr/bin/env python 
# coding:utf-8
# @Time :1/9/19 12:02

from www_yizhoucp_cn.spiders.yizhoucp_crawl import YizhoucpCrawl
from common.logger import AppLogger
import click

@click.command()
@click.option('--secrite_key',
              type=str,
              help=u'secrite_key')
@click.option('--token',
              type=str,
              help=u'token')
@click.option('--user_id',
              type=str,
              help=u'用户id')
@click.option('--check_code',
              type=str,
              help=u'check_code')
def main(secrite_key, token, user_id, check_code):
    log = AppLogger("yizhou_cp.log").get_logger()
    YizhoucpCrawl(secrite_key, token, user_id, check_code, log=log).start()

if __name__ == '__main__':
    main()
