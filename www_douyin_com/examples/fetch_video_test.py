#!/usr/bin/env python 
# coding:utf-8


from www_douyin_com.spiders.user_post import post
from www_douyin_com.handlers import FileHandler
from www_douyin_com.downloaders import VideoDownloader


def main():
    file_handler = FileHandler("./videos")
    video_downloader = VideoDownloader(handlers=[file_handler])

    for objs in post(user_id="61663533492"):
        video_downloader.download(objs)


if __name__ == '__main__':
    main()
