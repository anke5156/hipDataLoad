#!/usr/bin/python
# -*- coding: UTF-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.header import Header

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      sendEmail.py
@time:      2020/4/27 10:11 AM

@desc:      
'''


class Mail(object):
    def __init__(self):
        self.mailhost = 'smtp.qq.com'
        self.mailport = '465'
        self.mailuser = 'anke.wang@foxmail.com'
        self.mailpass = ''
        self.receiver = 'anke.wang@foxmail.com'

    def send(self, subjecttxt='NB Health Report', ctt=''):
        message = MIMEText(ctt, 'plain', 'utf-8')
        message['from'] = Header('NB office', 'utf-8')
        message['to'] = Header('Monitor', 'utf-8')
        message['Subject'] = Header(subjecttxt, 'utf-8')
        try:
            smtpObj = smtplib.SMTP(self.mailhost, self.mailport)
            # smtpObj.ehlo()
            # smtpObj.starttls()
            smtpObj.login(self.mailuser, self.mailpass)
            smtpObj.sendmail(self.mailuser, self.receiver, message.as_string())
            smtpObj.quit()
            print('send mail successfully!')
        except smtplib.SMTPException as e:
            print('send mail error: %s' % e)


if __name__ == '__main__':
    mail = Mail()
    mail.send('NB Health Report', 'ALL Healthy')
