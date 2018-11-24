#!/usr/bin/env python 
# coding:utf-8
# @Time :11/24/18 17:35

from enum import Enum


class DoubanRent:

    rent_status = ["已租", "删除"]

    bedroom = ["主卧", "次卧"]

    sex = ["男女", "女", "男"]


if __name__ == '__main__':
    print(DoubanRent.bedroom)
