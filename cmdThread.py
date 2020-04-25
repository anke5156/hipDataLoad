#!/usr/bin/python
# -*- coding: UTF-8 -*-

from threading import Thread
import subprocess
import logging

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      cmdThread.py
@time:      2020/4/25 11:25 AM

@desc:      为任务创建线程
'''


class CmdThread(Thread):
    def __init__(self, id, cmd):
        Thread.__init__(self)
        self.id = id
        self.cmd = cmd
        self.isSuccess = False

    def run(self):
        isComeon = True
        if isComeon:
            status = 0
            result = ''
            # logging.info(self.cmd)
            status, result = subprocess.getstatusoutput(self.cmd)
            if status == 0:
                logging.info('[****命令【%s】执行成功，退出进程!****]' % self.cmd)
                logging.info('[****执行结果【%s】****]' % result)
                self.isSuccess = True
            else:
                logging.info('[****命令【%s】执行失败! status=【%d】 result=【%s】进程退出!****]' % (
                    self.cmd, status, result))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename='./logs/test.log',
                        filemode='a'
                        )
    cm = CmdThread(1, "pwd",)
    cm.run()
