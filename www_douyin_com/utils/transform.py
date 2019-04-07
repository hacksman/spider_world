#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.structures import (Video, User)
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
    return Video(id=id,
                 desc=desc,
                 play_url=play_url,
                 user_info=user_info) if id else None


