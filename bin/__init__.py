#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bin.logger import Logger

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      logger.py
@time:      2020年04月29日23:19:18

@desc:      
'''

logger = Logger().logger


def info(msg):
    logger.info(msg)


def debug(msg):
    logger.debug(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)


def critical(msg):
    logger.critical(msg)
