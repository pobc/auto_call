import re
from datetime import datetime, timedelta

from utils import time_tools
from utils.DBUtils import DBUtils
import time


def sava_batch(data: list):
    sql = f"""insert into config_dict(title, price, img_data, insert_datetime) 
              values({'%s,' * 3} DATETIME('now','localtime'))"""
    return DBUtils.executeMany(sql=sql, args=data)


def insert_list_batch(data: list):
    # 编码  zl租赁地址
    fields = "itemId,`desc`,imageUrls,lastVisitTimeDesc,price,locationDetails,priceUnit,title," \
             "trackParams"
    fields_arr = fields.split(',')
    param_mark = "%s," * (len(fields_arr))
    param_mark = param_mark[:-1]
    sql = f"insert into config_dict ( {fields} ) values({param_mark})"
    total_house_data = []
    for dd in data:
        temp_data = []
        for fd in fields_arr:
            if fd == 'imageUrls':
                temp_data.append(dd['cardData'][fd][0])
            elif fd == '`desc`':
                temp_data.append(dd['cardData']['desc'])
            else:
                if type(dd['cardData'][fd]) is dict:
                    temp_data.append(str(dd['cardData'][fd]))
                else:
                    temp_data.append(dd['cardData'][fd])
        total_house_data.append(tuple(temp_data))
    time.sleep(2)
    if len(total_house_data) > 0:
        result = DBUtils.executeMany(sql, total_house_data)
        return {'code': 1, 'msg': f'保存数据量：{result} 条'}
    else:
        return {'code': -3, 'msg': "数据库执行sql有误"}


def insert_detail(data):
    # 编码  zl租赁地址
    fields = """itemId,browseCnt,wantCnt,`desc`,GMT_CREATE_DATE_KEY,nick"""
    fields_arr = fields.split(',')
    param_mark = "%s," * (len(fields_arr))
    param_mark = param_mark[:-1]
    sql = f"insert into config_dict({fields}) " \
          f"values({param_mark})"
    total_house_data = []
    temp_data = []
    for fd in fields_arr:
        if fd == '`desc`':
            temp_data.append(data['desc'])
        else:
            temp_data.append(data[fd])
    total_house_data.append(tuple(temp_data))
    if len(total_house_data) > 0:
        count = DBUtils.execute(sql, total_house_data[0])
        return {'code': 1, 'msg': f'保存详情数据量：{count} 条', 'wantCnt': data['wantCnt'],
                'browseCnt': data['browseCnt'], 'nick': data['nick']}
    else:
        return {'code': -3, 'msg': "数据库执行详情sql有误"}


def insert_msg(data):
    fields = """userId,fishNick,userMsgText,myMessage,itemId"""
    fields_arr = fields.split(',')
    param_mark = "%s," * (len(fields_arr))
    param_mark = param_mark[:-1]
    sql = f"insert into config_dict({fields}) values({param_mark}) "
    count = DBUtils.execute(sql, tuple(data))
    return {'code': 1, 'msg': f'保存聊天数据量：{count} 条'}


def query_new_house(events_name):
    sql = """
        SELECT *
        FROM config_dict
        WHERE insert_datetime >= (select insertDatetime from eventsLog where eventName=%s order by id desc limit 1)
        AND info_status is null
        AND itemId NOT IN (
            SELECT itemId
            FROM house_list
            WHERE insert_datetime < (select insertDatetime from eventsLog where eventName=%s order by id desc limit 1)
        )
    """
    #  and (lastVisitTimeDesc like '%%小时' or lastVisitTimeDesc in ('1天前'))
    return DBUtils.execute(sql, args=[events_name, events_name])


def delete_yesterday_duplicate_data():
    table_name = 'config_dict'
    backup_table(table_name)

    print(f'执行{table_name}表删除数据')
    sql = f"""
        DELETE FROM {table_name} WHERE id IN (
            SELECT * FROM (
                SELECT hl1.id
                FROM {table_name} hl1
                JOIN {table_name} hl2
                ON hl1.itemId = hl2.itemId AND hl1.id > hl2.id
                WHERE hl1.insert_datetime < %s
             ) AS tmp 
        )
    """
    return DBUtils.execute(sql, args=time_tools.get_previous_date(1).strftime('%Y-%m-%d'))


def backup_table(table_name):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_table_name = f"{table_name}_{current_time}"
    # 创建新表并复制数据
    backup_query = f"CREATE TABLE {backup_table_name} AS SELECT * FROM {table_name}"
    return DBUtils.execute(backup_query)


def delete_history_table(table_name):
    threshold_date = datetime.now() - timedelta(days=5)
    threshold_str = threshold_date.strftime("%Y%m%d%H%M%S")
    # 获取所有表名
    tables = DBUtils.queryNoDict("SHOW TABLES")
    # 正则表达式匹配备份表名
    pattern = re.compile(f"{table_name}_(\\d{{14}})")
    for table in tables:
        table_name = table[0]
        match = pattern.match(table_name)
        if match:
            backup_date_str = match.group(1)
            print(table)
            if backup_date_str < threshold_str:
                # 删除旧备份表
                delete_query = f"DROP TABLE {table_name}"
                DBUtils.execute(delete_query)


def query_last_config_info(item_id):
    sql = "select * from config_dict where key_val= %s order by id desc limit 1"
    return DBUtils.execute(sql, item_id)


def update_house_list(key_val, val):
    sql = "update config_dict set val=%s where key_val=%s"
    return DBUtils.execute(sql, args=[val, key_val])


def query_last_info(craw_time):
    sql = "select * from config_dict where insert_datetime > %s order by id desc limit 1"
    return DBUtils.execute(sql, craw_time)


def query_last_list(item_id):
    sql = "select * from config_dict where itemId= %s order by id desc limit 1"
    return DBUtils.execute(sql, item_id)


def del_last_crawler_data():
    sql = "DELETE FROM config_dict WHERE insert_datetime >= (SELECT insertDatetime FROM eventslog where eventName='xianyu_monitor' ORDER BY id DESC limit 1)"
    return DBUtils.execute(sql)


if __name__ == '__main__':
    print(len(()))
    # print(query_last_info('2024-5-28 15:36:00'))
    # query_new_house('2024-05-30 20:46:29')
    print(query_last_house_detail('781098050444'))
