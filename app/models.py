# -*- coding: utf-8 -*-
from datetime import datetime

from peewee import MySQLDatabase, DateTimeField, Model, CharField, BooleanField, IntegerField, AutoField, \
    ForeignKeyField
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from main.config import config
import os
import logging

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE, port=3306)
# 配置日志
logger = logging.getLogger('peewee')  # 获取 peewee 的日志记录器
logger.addHandler(logging.StreamHandler())  # 将日志处理程序添加到标准输出
logger.setLevel(logging.DEBUG)  # 设置日志级别为 DEBUG，这样会输出 SQL 日志


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


# 管理员工号
class MyUser(UserMixin, BaseModel):
    username = CharField()  # 用户名
    password = CharField()  # 密码
    fullname = CharField()  # 真实性名
    email = CharField()  # 邮箱
    phone = CharField()  # 电话
    status = BooleanField(default=True)  # 生效失效标识

    class Meta:
        table_name = 'my_user'

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


# 通知人配置
class CfgNotify(BaseModel):
    check_order = IntegerField()  # 排序
    notify_type = CharField()  # 通知类型：MAIL/SMS
    notify_name = CharField()  # 通知人姓名
    notify_number = CharField()  # 通知号码
    status = BooleanField(default=True)  # 生效失效标识

    class Meta:
        table_name = 'cfg_notify'


class SpeechPhoneNum(BaseModel):
    id = IntegerField()
    phone_num = CharField()
    phone_num2 = CharField()
    phone_status = CharField()
    house_area = CharField()
    task_code = CharField()
    house_num = CharField(null=True)
    update_datetime = DateTimeField(default=datetime.now)
    insert_datetime = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'speech_phone_num'


class SpeechAudioRecord(BaseModel):
    id = AutoField()
    phone_num = CharField()
    audio_file_name = CharField(max_length=255, null=True)
    call_datetime = DateTimeField()
    talk_times = IntegerField(null=True)
    duration = IntegerField(null=True)
    audio_txt = CharField(max_length=1000, null=True)
    intention_level = IntegerField(null=True)
    is_checked = IntegerField(null=True)
    insert_datetime = DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'speech_audio_record'
        indexes = (
            (('insert_datetime',), False),  # Create an index on insert_datetime
        )


class CallTask(BaseModel):
    id = AutoField()
    task_code = IntegerField(null=True)
    area_name = CharField(max_length=255, null=True)
    task_status = CharField(max_length=255, null=True)
    default_choose = CharField(max_length=255, null=True)
    insert_datetime = DateTimeField(default=datetime.now())
    update_datetime = DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'call_task'


class SpeechWord(BaseModel):
    """
    话术关键词模型
    Peewee 会自动创建一个名为 'id' 的自增主键。
    """
    txt = CharField(verbose_name="话术内容")
    txt_no = CharField(verbose_name="话术编号")
    ok_no = CharField(verbose_name="肯定回复编号")
    no_no = CharField(verbose_name="否定回复编号")
    hesitate_no = CharField(verbose_name="回复编号")
    community_name = CharField(verbose_name="社区名称")
    keys = CharField(verbose_name="关键词")
    insert_datetime = DateTimeField(default=datetime.now(), verbose_name="创建时间")
    update_datetime = DateTimeField(default=datetime.now(), verbose_name="更新时间")

    class Meta:
        # 指定数据库中的表名为 'speech_word'
        table_name = 'speech_word'


@login_manager.user_loader
def load_user(user_id):
    return MyUser.get(MyUser.id == int(user_id))


# 建表
def create_table():
    db.connect()
    print("创建表")
    db.create_tables([CfgNotify, MyUser])


if __name__ == '__main__':
    create_table()
