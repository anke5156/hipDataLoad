#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
from logging import handlers

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      config.py
@time:      2020/4/29 2:18 下午

@desc:      
'''

__version__ = '0.0.1'


class LoggerPro(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, fileName='../logs/hipdataload.log'):
        self.fileName = fileName
        self.logger = logging.getLogger(fileName)

    def config(self, level='info', when='D', backCount=30):
        """
        # midnight 每天凌晨
        :param level: debug,info,warning,error,critical
        :param when: 间隔的时间单位，单位有以下几种：
                    S 秒
                    M 分
                    H 小时、
                    D 天、
                    W 每星期（interval==0时代表星期一）
                    midnight 每天凌晨
        :param backCount: 备份文件的个数，如果超过这个个数，就会自动删除
        :return:
        """
        format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        format_str = logging.Formatter(format)  # 设置日志格式
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        # 实例化TimedRotatingFileHandler
        th = handlers.TimedRotatingFileHandler(filename=self.fileName, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器

        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


logger = LoggerPro().logger

if __name__ == '__main__':
    LoggerPro().config(level='debug')
    logger.debug('debug')
    logger.info('info')
    logger.warning('警告')
    logger.error('报错')
    logger.critical('严重')
