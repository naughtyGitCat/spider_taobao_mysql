#!/home/dba/python3/bin/python
# encoding=utf-8


# @Time    : 2018/10/7 下午4:31
# @Author  : 张锐志
# @TODO    : buy a house,live with a dog

# 系统库
import os
import sys
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
# 第三方库

from logbook.more import ColorizedStderrHandler
from logbook import Logger, TimedRotatingFileHandler,set_datetime_format

# 自定义库
depend_path = os.path.abspath(os.path.join('../common'))
sys.path.append(depend_path)
from config import EmailMisc

# 禁止from xx import *
__all__ = []

# 定义Logger
logger = Logger('utils')
# logger.handlers.append(TimedRotatingFileHandler(log_name, level=log_level, bubble=True, date_format='%Y-%m-%d',))
logger.handlers.append(ColorizedStderrHandler(level='DEBUG', bubble=True))


class MailClient(object):
    def __init__(self):
        self.message = MIMEMultipart()
        self.message['From'] = EmailMisc.sender
        self.message['To'] = EmailMisc.receivers
        self.server = smtplib.SMTP(EmailMisc.smtp_server)
        self._login()

    def _login(self):
        self.server.ehlo()
        self.server.login(EmailMisc.user, EmailMisc.password)

    def subject_body(self, subject='邮件标题', body='邮件正文'):
        """
        定义邮件标题和正文
        :param subject:
        :param body:
        :return:
        """
        self.message['Subject'] = subject
        self.message.attach(MIMEText(body, 'plain', 'utf-8'))

    def attach_file(self, file_type='file', target='', suffix='md'):
        """
        追加附件
        :param suffix: 文件后缀名,String类型直接引入时使用
        :param file_type: 文件类型,文件或者string对象
        :param target:目标文件位置或者string对象名称
        :return:无返回
        """
        if file_type == 'file':
            attach = MIMEText(open(target, 'rb').read(), 'base64', 'utf-8')
            attach_name = os.path.split(target)[-1]  # 附件文件名为实际的文件名
            attach.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attach_name))
        elif file_type == 'string':
            attach = MIMEText(target)
            attach_name = self.message['Subject']+'.'+suffix  # 附件文件名为传入为网页标题
            attach.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attach_name))
        attach['Content-Type'] = 'application/octet-stream'
        self.message.attach(attach)

    def send_mail(self):
        """
        发送邮件
        :return:
        """
        try:
            self.server.sendmail(EmailMisc.user, EmailMisc.receivers, self.message.as_string())
            self.server.quit()
        except Exception as e:
            print(traceback.format_exc())
            logger.error(e)

