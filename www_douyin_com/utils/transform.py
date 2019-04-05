#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.structures.videos import Video


def data_to_video(data):
    id = data.get("aweme_id")
    desc = data.get("desc")
    play_url = data.get("play_url")

    return Video(id=id,
                 desc=desc,
                 play_url=play_url) if id else None


