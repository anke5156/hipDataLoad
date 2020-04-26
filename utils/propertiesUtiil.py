#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os
import tempfile

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      propertiesUtiil.py
@time:      2020/4/26 10:26 AM

@desc:      
'''


class Properties:
    def __init__(self, configName='../config.perporties'):
        self.perporties_name = configName
        self.properties = {}
        try:
            with open(self.perporties_name, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.find('=') > 0 and not line.startswith('#'):
                        strs = line.split('=')
                        self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            f.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=None):
        if key in self.properties:
            return self.properties[key]
        return default_value


if __name__ == '__main__':
    pro = Properties()
    print(pro.has_key('rrrr'))
    print(pro.has_key('test1'))
    print(pro.get("test1"))
    print(pro.get("test2"))
