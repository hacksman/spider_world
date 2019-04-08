#!/usr/bin/env python 
# coding:utf-8


from www_douyin_com.structures import Base


class Statistic(Base):
    def __init__(self, **kwargs):
        super().__init__()
        self.id = kwargs.get("id")
        self.comment_count = kwargs.get("comment_count")
        self.digg_count = kwargs.get("digg_count")
        self.download_count = kwargs.get("download_count")
        self.play_count = kwargs.get("play_count")
        self.share_count = kwargs.get("share_count")
        self.forward_count = kwargs.get("forward_count")

    def __repr__(self):
        return "<Statistic: <%s>>" % self.id
