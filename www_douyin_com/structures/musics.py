#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.structures.base import Base


class Music(Base):

    def __init__(self, **kwargs):
        super().__init__()
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.play_url = kwargs.get("play_url")
        self.duration = kwargs.get("duration")
        self.owner_nickname = kwargs.get("owner_nickname")
        self.owner_id = kwargs.get("owner_id")
        self.cover_url = kwargs.get("cover_url")

    def __repr__(self):
        return "<Music: <%s, %s>>" % (self.id, self.name[:20].strip() if self.name else None)
