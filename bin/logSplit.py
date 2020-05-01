#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      logSplit.py
@time:      2020/4/26 9:13 AM

@desc:      日志切割模块，将日志切割成每日日志文件
'''


def splitlog(filename, mark):
    isStart = False
    # logNameDaily = '%s.%s' % (filename, time.strftime('%Y-%m-%d'))
    # logDaily = open(logNameDaily, 'w')

    logNameCmdsDaily = '%s.cmd.%s' % (filename, time.strftime('%Y-%m-%d'))
    logDailyExcute = open(logNameCmdsDaily, 'w')
    with open(filename, 'r+') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.find(mark) != -1:
                isStart = True
            if isStart:
                # logDaily.write('%s' % line)
                if (line.find('EXCUTE_DONE') != -1):
                    logDailyExcute.write('%s' % line)
        f.close()
        # logDaily.close()
        logDailyExcute.close()


if __name__ == '__main__':
    splitlog('../logs/hipdataload.log', '1587863489.224271')
