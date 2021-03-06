#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os
import sys

sys.path.append('..')
from script.checkMaping import ChcekMapping
from bin.loggerPro import LoggerPro, logger

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      hipDataLoad.py
@time:      2020/4/23 11:26 AM

@desc:
'''


class ExploteSql(object):
    def __init__(self, fileName):
        self.fileName = fileName
        assert ChcekMapping().checkJson(self.fileName)
        # 校验配置的mapping数据格式
        with open(self.fileName, 'r', encoding='utf-8') as f:
            # 将类文件对象中的JSON字符串直接转换成Python字典
            self.jBase = json.load(f)
            # 获取json中的表信息
            self.source = self.jBase['source']
            self.database = self.jBase['database']
            self.table = self.jBase['table']
            # 字段映射成身份证号、邮箱、手机号、、、
            self.jField = self.jBase['fieldMapping']
            self.uuid = self.jField['uuid']
            self.sfzh = self.jField['sfzh']
            self.user_name = self.jField['user_name']
            self.email = self.jField['email']
            self.phoneno = self.jField['phoneno']
            self.password = self.jField['password']
            self.explode_time = self.jField['explode_time']
            self.confidence = self.jField['confidence']
            self.source_table = self.table

    def _ruleMatching(self, col, rule, position):
        """
        规则转换，对json定义的字段规则进行转换,输出转换后的字段
        :param col: 需要做规则转换的列名称
        :param rule:转换规则 where条件不为空：not_null；查询处理null:convert_empty,该规则根据实际情况可以不断新增 
        :param position:1.处理查询字段，2.处理where条件为空，3.计算置信度 
        :return: 根据规则转换之后的列名称
        eg:1：case when tag6='' or upper(tag6)='NULL' then null else tag6 end
           2：and upper(trim(tag6))!='NULL' and trim(tag6)!='' and tag6 is not null
        """
        c = ''
        if (rule is None):
            c = col
        elif (position == 2 and rule.__contains__('not_null')):
            c = format("and upper(trim(%s))!='NULL' and trim(%s)!='' and %s is not null" % (col, col, col))
        elif (position == 1 and rule.__contains__('convert_empty')):
            c = format("case when trim(%s)='' or upper(trim(%s))='NULL' then null else trim(%s) end as %s"
                       % (col, col, col, col))
        elif (position == 1 and rule.__contains__('confidence')):
            """
                首先判断身份证手机号,俩都有               0.9
                有身份证或手机号其中一个                  0.8
                没有身份证手机号，判断邮箱，有邮箱          0.5
                没有身份证手机号没有邮箱，有用户名和密码	   0.5
                没有身份证手机号没有邮箱没有密码，只有用户名  0.3
                其他	                                   0.2
            """
            c = 'case'
            if (self.phoneno != '' and self.sfzh != ''):
                c = format(
                    "%s when length(trim(%s))=11 and substr(trim(%s),1,1)='1' and length(trim(%s)) in (15,18) then '0.9' "
                    "when length(trim(%s))=11 and substr(trim(%s),1,1)='1' or length(trim(%s)) in (15,18) then '0.8'"
                    % (c, self.phoneno, self.phoneno, self.sfzh, self.phoneno, self.phoneno, self.sfzh))
            elif (self.phoneno == '' and self.sfzh != ''):
                c = format("%s when length(trim(%s)) in (15,18) then '0.8'" % (c, self.sfzh))
            elif (self.phoneno != '' and self.sfzh == ''):
                c = format(
                    "%s when length(trim(%s))=11 and substr(trim(%s),1,1)='1' then '0.8'"
                    % (c, self.phoneno, self.phoneno))
            if (self.email != ''):
                c = format("%s when upper(trim(%s)) like '%s.COM%s' then '0.5'" % (c, self.email, '%', '%'))
            if (self.user_name != '' and self.password != ''):
                c = format("%s when trim(%s)!='' and trim(%s)!='' then '0.5'" % (c, self.user_name, self.password))
            if (self.user_name != ''):
                c = format("%s when trim(%s)!='' then '0.3' " % (c, self.user_name))
            if (self.sfzh == '' and self.phoneno == ''
                    and self.email == '' and self.user_name == ''):
                c = "'0.2'"
            else:
                c = format("%s else '0.2' end as %s" % (c, col))
        else:
            c = col
        return c

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
        email_ = "and upper(trim(email)) like '%.COM%'"
        user_name_ = "and user_name!=email and upper(trim(user_name))!='NULL' and trim(user_name)!='' and user_name is not null"
        password_ = "and upper(trim(password))!='NULL' and trim(password)!='' and password is not null"
        s1 = ''
        s2 = ''
        sql = ''
        if (targetType == '20'):
            sql = format("insert into table sgk.t_ml_sgk_small_merge_%s "
                         "(uuid,sfzh,user_name,email,phoneno,password,explode_time,confidence,source_table,source) "
                         "select %s from sgk_source.%s "
                         "where 1=1 ;"
                         % (self.source, cols, self.table))
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
                logger.error('参数错误，请检查！')
            sql = format("-- insert into table sgk.t_ml_sgk_relation "
                         "select uuid,%s,'%s',confidence "
                         "from sgk.t_ml_sgk_small_merge_%s "
                         "where 1=1 %s %s ;"
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
        col = []
        # 获取json中的字段，并拼接字符串
        for k, v in self.jField.items():
            # 获取json中配置的字段规则，并进行字段转换
            rul = self.jBase['rule'].get(v)
            v_ = self._ruleMatching(v, rul, 1)
            v_ = v_ if v_ != '' else 'null'
            if (k in ['source', 'source_table']):
                v_ = f"'{v_}'"
            col.append(v_)
        c2_ = ','.join(col)
        return self._buildSql(c2_, targetType)


if __name__ == '__main__':
    LoggerPro().config()
    for dirPath, dirNames, fileNames in os.walk('../mappings'):
        for fileName in fileNames:
            if fileName.endswith('json'):
                i = os.path.join(dirPath, fileName)
                with open(i, 'r') as f:
                    c = ExploteSql(f.name)
                    logger.info(f'正在处理【{f.name}】文件')
                    if not os.path.isdir('../sql'):  # 无文件夹时创建
                        os.makedirs('../sql')
                    file = os.path.join('../sql', c.table + '.sql')
                    lis = ['20', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

                    with open(file, mode="w+", encoding="utf-8") as fd:
                        for i in lis:
                            fd.write(c.getSql(i))
                            fd.write('\n\n')
                        fd.flush()
                        fd.close()
