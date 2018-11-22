#!/usr/bin/env python 
# coding:utf-8
# @Time :11/22/18 09:22


class URL:
    COMMON_URL = "https://aweme.snssdk.com/aweme/v1/"

    @classmethod
    def follow_url(cls):
        return cls.COMMON_URL + "user/following/list/"

    @classmethod
    def user_video_url(cls):
        return cls.COMMON_URL + "aweme/post/"

    @classmethod
    def video_detail_url(cls):
        return cls.COMMON_URL + "aweme/detail/"

    @classmethod
    def favorite_url(cls):
        return cls.COMMON_URL + "aweme/favorite/"

    @classmethod
    def post_url(cls):
        return cls.COMMON_URL + "aweme/post/"

    @classmethod
    def comment_url(cls):
        return cls.COMMON_URL + "comment/list/"

    @classmethod
    def music_url(cls, music_id):
        return "https://p3.pstatp.com/obj/" + music_id

    @classmethod
    def like_video_url(cls):
        return cls.COMMON_URL + "commit/item/digg/"

