#!/usr/bin/env python 
# coding:utf-8
# @Time :11/24/18 18:18

from enum import Enum

class RentStatus(Enum):
    ONLINE = 1
    DOWNLINE = 0

class HostNeedRentStatus(Enum):
    YES = 1
    NO = -1
    UNKNOW = 0

class HostIsPersonal(Enum):
    YES = 1
    NO = -1
    UNKNOW = 0

class AttrExistStatus(Enum):
    YES = 1
    NO = -1
    UNKNOW = 0