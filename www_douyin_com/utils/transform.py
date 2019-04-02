#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.structures.videos import Video

def data_to_video(data):
    id = data.get("aweme_id")
    desc = data.get("desc")

    return Video(id=id,
                 desc=desc) if id else None


