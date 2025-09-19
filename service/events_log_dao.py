from utils.DBUtils import DBUtils


def insert_log(event_name):
    return DBUtils.execute('insert into eventsLog (eventName) values (%s)', event_name)


def query_last_log(event_name):
    return DBUtils.execute('select * from eventsLog where eventName=%s order by id desc limit 1', event_name)
