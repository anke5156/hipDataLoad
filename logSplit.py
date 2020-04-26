#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import os
from utils.propertiesUtiil import Properties

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      logSplit.py
@time:      2020/4/26 9:13 AM

@desc:      日志切割模块，将日志切割成每日日志文件
'''


def splitlog(filename, mark):
    isStart = False
    logFileDaily = '%s.%s' % (filename, time.strftime('%Y-%m-%d'))
    newlog = open(logFileDaily, 'w')
    # newlog = open(ddd, 'w')
    with open(filename, 'r+') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.find(mark) != -1:
                isStart = True
            if isStart:
                newlog.write('%s' % line)
        f.close()
        newlog.close()


if __name__ == '__main__':
    splitlog('./logs/test.log', '1587863489.224271')
