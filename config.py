#! /usr/bin/python3
# encoding=utf-8


# @Time    : 2018/10/7 下午4:33
# @Author  : 张锐志
# @TODO    : buy a house,live with a dog

# 系统库

# 第三方库

# 自定义库

# 禁止from xx import *
__all__ = []


class EmailMisc(object):
    sender = "me@lonely.com"               # 发件人，有些邮箱可以自定义，但建议和user相同
    receivers = 'u@dream.com'              # 收件人，不要写多个收件人，容易被退信
    user = 'me@lonely.com'                 # 发件人，账号，有些设置了别名或者手机号的，请用原本的账号
    password = 'fall_in_sleep'             # 发件人，密码
    smtp_server = 'smtp.bed.com'           # 发件人，smtp服务地址，部分邮箱需要开通smtp发信服务


class MetaMisc(object):                    # 元信息上传
    user = "guest"                         # mysql用户名
    pwd = 'hello'                          # mysql密码
    host = '0.0.0.0'                       # mysql主机
    port = 3306                            # mysql端口
    db = 'library'                         # 库
    tb = 'taobao_monthly_report'           # 表


class OtherMisc(object):
    archive_dir = '/tmp'  # 归档地址

