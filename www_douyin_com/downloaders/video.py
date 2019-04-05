#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.downloaders import Downloader
from www_douyin_com.handlers import Handler


class VideoDownloader(Downloader):

    async def process_item(self, obj):
        print("Process...", obj, "...")
        for handler in self.handlers:
            if isinstance(handler, Handler):
                await handler.process(obj)
