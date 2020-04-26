#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import logging

from bin.checkMaping import chcekJson
from bin.propertiesUtiil import Properties

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      hipDataLoad.py
@time:      2020/4/23 11:26 AM

@desc:
'''


class Mapping(object):
    def __init__(self, fileName):
        self.fileName = fileName

        with open(self.fileName, 'r', encoding='utf-8') as f:
            # 将类文件对象中的JSON字符串直接转换成Python字典
            self.mapstr = json.load(f)
            # 校验配置的mapping数据格式
            assert chcekJson().check(self.mapstr)
            # 获取json中的表信息
            self.source = self.mapstr['source']  # 数据源eg:12306,hanting,zhenaiwang...
            self.database = self.mapstr['database']
            self.table = self.mapstr['table']
            # 字段映射成身份证号、邮箱、手机号、、、
            self.mapping_ = self.mapstr['fieldMapping']
            self.uuid = self.mapping_['uuid']
            self.sfzh = self.mapping_['sfzh']
            self.user_name = self.mapping_['user_name']
            self.email = self.mapping_['email']
            self.phoneno = self.mapping_['phoneno']
            self.password = self.mapping_['password']
            self.explode_time = self.mapping_['explode_time']
            self.confidence = self.mapping_['confidence']
            self.source_table = self.mapping_['source_table']

    def _ruleMatching(self, col, rule, position):
        """
        规则转换，对json定义的字段规则进行转换,输出转换后的字段
        :param col: 需要做规则转换的列名称
        :param rule:转换规则 where条件不为空：not_null；查询替换空为null:convert_empty,该规则根据实际情况可以不断新增 
        :param position:1.处理查询字段，2.处理where条件为空，3.计算置信度 
        :return: 根据规则转换之后的列名称
        eg:1：case when tag6='' or upper(tag6)='NULL' then null else tag6 end
           2：and upper(trim(tag6))!='NULL' and trim(tag6)!='' and tag6 is not null
        """
        if (rule is None):
            return col
        elif (position == 1 and rule.__contains__('convert_empty')):
            return format("case when trim(%s)='' "
                          "or upper(trim(%s))='NULL' then null "
                          "else %s end as %s" % (col, col, col, col))
        elif (position == 2 and rule.__contains__('not_null')):
            return format("and upper(trim(%s))!='NULL' "
                          "and trim(%s)!='' "
                          "and %s is not null" % (col, col, col))
        elif (position == 1 and rule.__contains__('confidence')):
            return format(
                "case when length(trim(%s))=11 and substr(%s,1,1)='1' and length(trim(%s)) in (15,18) then '0.9' "
                "when length(trim(%s))=11 and substr(%s,1,1)='1' or length(trim(%s)) in (15,18) then '0.8' "
                "else 0.5 end as %s" % (
                    self.phoneno, self.phoneno, self.sfzh, self.phoneno, self.phoneno, self.sfzh, col))
        else:
            return col

    def _buildSql(self, cols, targetType):
        """
        拼接要插入目标表的sql
        :param self: 
        :param cols:字段字符串，select 后面的具体字段 
        :param targetType: 插入目标表类型
                           宽表:20,
                           关系表:01:身份证手机号关系；
                                02:身份证邮箱关系；
                                03:身份证用户名关系；
                                04:身份证密码关系；
                                05:手机号用户名关系；
                                06:手机号邮箱关系；
                                07:手机号密码关系；
                                08:邮箱用户名关系；
                                09:邮箱密码关系；
                                10:用户名密码关系
                                 
        :return: sql
        """
        sfzh_ = "and length(trim(sfzh)) in (15,18)"
        phoneno_ = "and length(trim(phoneno))=11 and substr(trim(phoneno),1,1)=1"
        email_ = "and email like '%.com'"
        user_name_ = "and user_name!=email and upper(trim(user_name))!='NULL' and trim(user_name)!='' and user_name is not null"
        password_ = "and upper(trim(password))!='NULL' and trim(password)!='' and password is not null"
        s1 = ''
        s2 = ''
        sql = ''
        if (targetType == '20'):
            sql = format("insert into table sgk.t_ml_sgk_small_merge_%s "
                         "(uuid,sfzh,user_name,email,phoneno,password,explode_time,confidence,source_table) "
                         "select %s  from %s.%s "
                         "where 1=1 "
                         % (self.source, cols, self.database, self.table))
        else:
            if (targetType == '01'):
                sql = "sfzh,phoneno,'01'"
                s1 = sfzh_
                s2 = phoneno_
            elif (targetType == '02'):
                sql = "sfzh,email,'02'"
                s1 = sfzh_
                s2 = email_
            elif (targetType == '03'):
                sql = "sfzh,user_name,'03'"
                s1 = sfzh_
                s2 = user_name_
            elif (targetType == '04'):
                sql = "sfzh,password,'04'"
                s1 = sfzh_
                s2 = password_
            elif (targetType == '05'):
                sql = "phoneno,user_name,'05'"
                s1 = phoneno_
                s2 = user_name_
            elif (targetType == '06'):
                sql = "phoneno,email,'06'"
                s1 = phoneno_
                s2 = email_
            elif (targetType == '07'):
                sql = "phoneno,password,'07'"
                s1 = phoneno_
                s2 = password_
            elif (targetType == '08'):
                sql = "email,user_name,'08'"
                s1 = email_
                s2 = user_name_
            elif (targetType == '09'):
                sql = "email,password,'09'"
                s1 = email_
                s2 = password_
            elif (targetType == '10'):
                sql = "user_name,password,'10'"
                s1 = user_name_
                s2 = password_
            else:
                logging.info('参数错误，请检查！')
                exit(-1)
            sql = format("insert into table sgk.t_ml_sgk_relation "
                         "select uuid,%s,'%s',confidence "
                         "from sgk.t_ml_sgk_small_merge_%s "
                         "where 1=1 %s %s "
                         % (sql, self.table, self.source, s1, s2))
        return sql

    def getSql(self, targetType):
        """
        解析json文件,拼接可执行sql
        :param targetType: 
                           宽表:20,
                           关系表:01:身份证手机号关系；
                                02:身份证邮箱关系；
                                03:身份证用户名关系；
                                04:身份证密码关系；
                                05:手机号用户名关系；
                                06:手机号邮箱关系；
                                07:手机号密码关系；
                                08:邮箱用户名关系；
                                09:邮箱密码关系；
                                10:用户名密码关系
        :return: 拼接好的sql
        """
        assert isinstance(targetType, str)
        # with open(self.fileName, 'r', encoding='utf-8') as f:
        #     # 将类文件对象中的JSON字符串直接转换成Python字典
        #     mapstr = json.load(f)
        #     # 校验配置的mapping数据格式
        #     assert chcekJson().check(mapstr)
        #     # 获取json中的表信息
        #     self.source = mapstr['source']  # 数据源eg:12306,hanting,zhenaiwang...
        #     self.database = mapstr['database']
        #     self.table = mapstr['table']
        #     # 字段映射成身份证号、邮箱、手机号、、、
        #     mapping_ = mapstr['fieldMapping']
        #     self.uuid = mapping_['uuid']
        #     self.sfzh = mapping_['sfzh']
        #     self.user_name = mapping_['user_name']
        #     self.email = mapping_['email']
        #     self.phoneno = mapping_['phoneno']
        #     self.password = mapping_['password']
        #     self.explode_time = mapping_['explode_time']
        #     self.confidence = mapping_['confidence']
        #     self.source_table = mapping_['source_table']

        col = []
        # 获取json中的字段，并拼接字符串
        for k, v in self.mapping_.items():
            # 获取json中配置的字段规则，并进行字段转换
            rul = self.mapstr['rule'].get(v)
            v_ = self._ruleMatching(v, rul, 1)
            col.append(v_)
        c2_ = ','.join(col)
        return self._buildSql(c2_, targetType)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename=Properties('../config/config.perporties').get("logFile"),
                        filemode='a'
                        )
    c = Mapping(fileName='../mappings/tb_ml_test.json')
    print(c.getSql('20'))
    print(c.getSql('01'))
    print(c.getSql('02'))
    print(c.getSql('03'))
    print(c.getSql('04'))
    print(c.getSql('05'))
    print(c.getSql('06'))
    print(c.getSql('07'))
    print(c.getSql('08'))
    print(c.getSql('09'))
    print(c.getSql('10'))
    # logging.info(c.ruleMatching('tag6', ["not_null", "convert_empty"], 1))
    # logging.info(c.ruleMatching('tag6', ["not_null", "convert_empty"], 2))
    # logging.info(c.ruleMatching('tag6', ["not_null", "convert_empty"], 3))
    # logging.info(c.ruleMatching('tag6', 'confidence', 1))
