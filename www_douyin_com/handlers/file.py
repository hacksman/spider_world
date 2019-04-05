#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.handlers import Handler
from www_douyin_com.utils.proxy import grab_proxy
from os.path import exists, join
from os import makedirs
import aiohttp


class FileHandler(Handler):

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        if not exists(self.folder):
            makedirs(self.folder)

    async def _process(self, obj, **kwargs):
        print("Downing...", obj, "...")
        kwargs.update({'ssl': False})
        kwargs.update({'timeout': 10})
        kwargs.update({"proxy": grab_proxy()})
        async with aiohttp.ClientSession() as session:
            async with session.get(obj.play_url, **kwargs) as response:
                if response.status == 200:
                    full_path = join(self.folder, "{}.mp4".format(obj.id))
                    with open(full_path, "wb") as f:
                        f.write(await response.content.read())
                    print("Downloaded file to", full_path)
                else:
                    print("Failed download %s, response status is %s" % (obj.id, response.status))

    async def process(self, obj, **kwargs):
        return await self._process(obj, **kwargs)
