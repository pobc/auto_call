import sqlite3 as lite
import json
import utils.time_tools as time_pretty
from datetime import datetime, timedelta


def insert_log(log_val=''):
    return insert_update(f"insert into botsLog(log) values(?)", [log_val])


def insert_login_log(log_val=''):
    return insert_update(f"insert into loginLog(log) values(?)", [log_val])


def query_login_log():
    lastMinute = datetime.strftime(datetime.now() + timedelta(minutes=-1), '%Y-%m-%d %H:%M:%S')
    return query_by_sql(f"select count(0) as errorTimes from loginLog where log like 'authError%' and insertTime > ?",
                        [lastMinute])


def update_dict(key_name='tradeStatus', key_val='on'):
    sql = f'update fmzConfig set keyVal=?,insertTime=DATETIME("now","localtime") where keyName=?'
    return insert_update(sql, [key_val, key_name])


def update_email_info(key_val='', key_name='lastEmail'):
    sql = f'update fmzConfig set keyVal=?,insertTime=DATETIME("now","localtime") where keyName=?'
    return insert_update(sql, [str(key_val), key_name])


def insert_update(sql=None, args: list = []):
    with lite.connect(config.sqlite_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, args)
        cursor.close()
        conn.commit()
        return cursor


def exec_sql(sql=None, args=None, isMany=False):
    with lite.connect(config.sqlite_db_path) as conn:
        cursor = conn.cursor()
        if isMany:
            cursor.executemany(sql, args)
        else:
            if args is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, args)
        result = cursor.rowcount
        cursor.close()
        conn.commit()
        return result


def exec_sql_many(sql=None, args: list = []):
    return exec_sql(sql, args, isMany=True)


def query_bots_log(table_name='botsLog', limit=10):
    return query_by_sql(f"select * from {table_name} order by id desc limit ?", [limit])


def format_log(log_info):
    log_info['personalTime'] = time_pretty.pretty_date(datetime.strptime(log_info['insertTime'], '%Y-%m-%d %H:%M:%S'))
    return log_info


def query_bots_log_pretty(table_name='botsLog', limit=5):
    bots_log = query_bots_log(table_name, limit)
    return [format_log(log) for log in bots_log]


def row_to_dict(cursor: lite.Cursor, row: lite.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data


def query_dict(key_name='tradeStatus') -> list:
    return query_by_sql(f"select keyName,keyVal,insertTime from fmzConfig where keyName=?", [key_name])


def query_dict_expire_val(keyName, defaultVal, expireHours=-24):
    lastDay = datetime.strftime(datetime.now() + timedelta(hours=expireHours), '%Y-%m-%d %H:%M:%S')
    configResult = query_by_sql(f"select keyVal,insertTime from fmzConfig where keyName=? and insertTime>?",
                                [keyName, lastDay])
    if configResult and len(configResult) > 0:
        return configResult[0]['keyVal']
    else:
        return defaultVal


def query_dict_val(key_name='tradeStatus'):
    result = query_dict(key_name=key_name)
    if result and len(result) > 0:
        result = result[0]['keyVal']
        if str(result).find("{") > -1:
            return json.loads(result.replace("\'", "\""))
        else:
            return result
    return None


def query_by_sql(sql='', args: list = [], withKey=True):
    with lite.connect(config.sqlite_db_path) as conn:
        if withKey:
            conn.row_factory = row_to_dict
        cursor = conn.cursor()
        cursor.execute(sql, args)
        query_info = cursor.fetchall()
        cursor.close()
        return query_info


def point_type(val):
    if val is not None:
        if type(val) is int or type(val) is float or type(val) is str:
            return val
        else:
            return str(val)
    return val
