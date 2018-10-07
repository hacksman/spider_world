#!/usr/bin/env python 
# coding:utf-8
# @Time :10/7/18 11:27


import sys
from logging.handlers import RotatingFileHandler

sys.path.append("..")
import logging
import os


def getLogger(task_name="root", level=logging.INFO, console_out=False):
    logger = logging.getLogger(task_name)
    if isinstance(level, str):
        level = level.lower()
    if level == "debug":
        level = logging.DEBUG
    elif level == "info":
        level = logging.INFO
    elif level == "warning":
        level = logging.WARNING
    elif level == "error":
        level = logging.ERROR
    else:
        level = logging.INFO

    if not os.path.exists("../logs"):
        os.makedirs("../logs")
    LOG_FILE = "../logs/%s.log" % task_name
    fmt = "%(asctime)s - %(filename)s[line:%(lineno)d] %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=64 * 1024 * 1025, backupCount=5, encoding='utf-8')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if console_out is True:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    logger.setLevel(level)
    return logger