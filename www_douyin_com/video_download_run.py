#!/usr/bin/env python 
# coding:utf-8
# @Time :10/11/18 21:03


import sys

sys.path.append('../')
sys.path.append('../../')

from www_douyin_com.spiders.douyin_crawl import DouyinCrawl

douyin_crawl = DouyinCrawl()

argv_execute = sys.argv[1:-1]

if len(sys.argv) < 3:
    print("请输入正确的参数：如 python video_download_run.py -one 6610886853165845773")

allow_execute = ["-one", "-ulike", "-upost", "-m"]

if not all(map(lambda x: x in allow_execute, argv_execute)):
    print("请输入正确的限制命令：当前仅支持 -one 、-m 、 -ulike 和 -upost")

if "-one" in argv_execute:
    print("正在下载...")
    douyin_crawl.download_one_video(sys.argv[-1])
    print("下载完成...")

if "-upost" in argv_execute:
    if not "-m" in argv_execute:
        douyin_crawl.grab_user_media(sys.argv[-1], "USER_POST")
    else:
        douyin_crawl.grab_user_media(sys.argv[-1], "USER_POST", content='-m')

if sys.argv[1] == "-ulike":
    if not "-m" in argv_execute:
        douyin_crawl.grab_user_media(sys.argv[-1], "USER_LIKE")
    else:
        douyin_crawl.grab_user_media(sys.argv[-1], "USER_LIKE", content='-m')
