#!/usr/bin/env python 
# coding:utf-8
# @Time :11/24/18 10:49


import logging
import os
from logging.handlers import RotatingFileHandler


class AppLogger(object):
    # 默认info级别
    level = logging.INFO

    # 存放目录名称
    folder = '../logs'

    def __init__(self, filename, for_mat=None):
        pwd = os.path.abspath(os.path.dirname(__file__))

        directory = os.path.join(pwd, self.folder)
        if not os.path.exists(directory):
            os.mkdir(directory)

        self.file_path = directory + '/' + filename

        self.log = logging.getLogger(filename)
        self.log.setLevel(self.level)

        handler = RotatingFileHandler(self.file_path, maxBytes=1024 * 1024 * 200, backupCount=10, encoding='utf-8')

        # 设置输出格式
        format_log = "%(asctime)s %(levelname)s %(filename)s %(funcName)s:%(lineno)s %(message)s"
        if for_mat is not None:
            format_log = for_mat
        fmt = logging.Formatter(format_log)
        handler.setFormatter(fmt)

        self.log.addHandler(handler)

        # 控制台输出
        stream = logging.StreamHandler()
        stream.setFormatter(fmt)

        self.log.addHandler(stream)

    def set_level(self, level):
        self.log.setLevel(level=level)
        return self.log

    def get_logger(self):
        return self.log

    def __del__(self):
        pass


if __name__ == '__main__':
    log = AppLogger('log.log').get_logger()
    log.info('text')
    log.warn('text')
    log.error('text')
