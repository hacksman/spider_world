#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.structures.base import Base


class Video(Base):

    def __init__(self, **kwargs):
        super().__init__()
        self.id = kwargs.get("id")
        self.desc = kwargs.get("desc")

    def __repr__(self):
        "<Video: <%s, %s>>" % (self.id, self.desc[:10].strip() if self.desc else None)

