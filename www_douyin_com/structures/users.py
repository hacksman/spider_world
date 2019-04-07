#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.structures import Base


class User(Base):
    def __init__(self, **kwargs):
        super().__init__()
        self.id = kwargs.get("id")
        self.nick_name = kwargs.get("nick_name")
        self.alias = kwargs.get("alias")
        self.gender = kwargs.get("gender")
        self.birthday = kwargs.get("id")
        self.sign = kwargs.get("sign")
        self.avatar = kwargs.get("avatar")

    def __repr__(self):
        return "<User: <%s, %s>>" % (self.id, self.nick_name)
