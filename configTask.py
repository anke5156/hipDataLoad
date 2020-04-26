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
            1: {'pwd': []},
            2: {'ls': ['pwd'], 'whoami': []},
            3: {'date': ['pwd', 'ls']}

        }
