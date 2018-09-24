#!/usr/bin/env python 
# coding:utf-8
# @Time :9/17/18 09:58

def china(start, end):
    for page in range(start, end + 1):
        yield 'http://tech.china.com/articles/index_' + str(page) + '.html'