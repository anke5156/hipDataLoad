#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      configTask.py
@time:      2020/4/23 3:03 PM

@desc:      configuration of the job
            目前是三级关系
            JOB->LAYER->TASK
            配置方式如下
            {
            LAYER1:{TASK1:[TASK1 relies], TASK2:[TASK2 relies]},
            LAYER2:{TASK3:[TASK3 relies], TASK4:[TASK4 relies]}
            }
'''


class ConfigTask(object):
    def __init__(self):
        self.cfg = {
            1: {'cmd1-1': []},
            2: {'cmd2-1': ['cmd1-1'],
                'cmd2-2': ['cmd2-3'],
                'cmd2-3': [],
                'cmd2-4': [],
                'cmd2-5': ['cmd2-4'],
                'cmd2-6': [],
                'cmd2-7': [],
                'cmd2-8': ['cmd2-2'],
                'cmd2-9': [],
                'cmd2-10': []},
            3: {'cmd3-1': ['cmd2-2']}
        }
