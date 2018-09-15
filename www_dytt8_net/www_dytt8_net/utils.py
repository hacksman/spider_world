#!/usr/bin/env python 
# coding:utf-8
# @Time :9/15/18 15:16

from os.path import realpath, dirname
import json


def get_config(name):
    path = dirname(realpath(__file__)) + "/configs/" + name + ".json"
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())
