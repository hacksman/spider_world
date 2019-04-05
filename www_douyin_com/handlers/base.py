#!/usr/bin/env python 
# coding:utf-8


class Handler(object):

    async def process(self, obj, **kwargs):
        raise NotImplementedError

