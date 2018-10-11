#!/usr/bin/env python 
# coding:utf-8
# @Time :10/11/18 21:03


import sys

sys.path.append('../')
sys.path.append('../../')

from www_douyin_com.spiders.douyin_crawl import DouyinCrawl

douyin_crawl = DouyinCrawl()

if len(sys.argv) < 3:
    print("请输入正确的参数：如 python video_download_run.py -one 6610886853165845773")

if len(sys.argv) != 3:
    print("请输入正确的参数：如 python video_download_run.py -one 6610886853165845773")

if not sys.argv[1] in ["-one", "-user"]:
    print("请输入正确的限制命令：如 -one 或 -user")

if sys.argv[1] == "-one":
    print("正在下载...")
    douyin_crawl.download_one_video(sys.argv[2])
    print("下载完成...")

if sys.argv[1] == "-user":
    douyin_crawl.grab_video(sys.argv[2], "USER_POST")
