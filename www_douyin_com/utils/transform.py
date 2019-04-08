#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.structures import (Video, User, Statistic, Music)
from www_douyin_com.utils.tools import first


def data_to_user(data):
    id = data.get("uid")
    nick_name = data.get("nickname")
    alias = data.get("unique_id") or data.get("short_id")
    gender = data.get("gender")
    birthday = data.get("birthday")
    sign = data.get("signature")
    avatar = first(data.get('avatar_larger', {}).get('url_list', []))

    return User(id=id,
                nick_name=nick_name,
                alias=alias,
                gender=gender,
                birthday=birthday,
                sign=sign,
                avatar=avatar) if id else None


def data_to_video(data):
    id = data.get("aweme_id")
    desc = data.get("desc")
    play_url = data.get("play_url")
    user_info = data_to_user(data.get("author", {}))
    statistic = data_to_statistic(data.get("statistics", {}))
    return Video(id=id,
                 desc=desc,
                 play_url=play_url,
                 user_info=user_info,
                 statistic=statistic) if id else None


def data_to_music(data):
    id = data.get("mid")
    name = data.get("title")
    play_url = first(data.get("play_url", {}).get("url_list", []))
    duration = data.get("duration")
    owner_nickname = data.get("owner_nickname")
    owner_id = data.get("owner_id")
    cover_url = first(data.get("cover_large", {}).get("cover_large", []))
    return Music(id=id,
                 name=name,
                 play_url=play_url,
                 duration=duration,
                 owner_nickname=owner_nickname,
                 owner_id=owner_id,
                 cover_url=cover_url) if id else None


def data_to_statistic(data):
    id = data.get("aweme_id")
    comment_count = data.get("comment_count")
    digg_count = data.get("digg_count")
    download_count = data.get("download_count")
    play_count = data.get("play_count")
    share_count = data.get("share_count")
    forward_count = data.get("forward_count")

    return Statistic(id=id,
                     comment_count=comment_count,
                     digg_count=digg_count,
                     download_count=download_count,
                     play_count=play_count,
                     share_count=share_count,
                     forward_count=forward_count) if id else None
