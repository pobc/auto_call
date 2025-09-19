import pymysql
import platform
# 连接mysql字符串
from main import config


def db():
    db = pymysql.connect(host=config.db_config['host'], user=config.db_config['user'], password=config.db_config['pwd'],
                         db=config.db_config['database'], port=config.db_config['port'], cursorclass=pymysql.cursors.DictCursor)
    return db


db = db()


class DBUtils:
    @staticmethod
    def execute(sql, args=None, exe_type=None):
        db.cursorclass = pymysql.cursors.DictCursor
        if sql:
            sql = sql.lstrip()
            # 增删改 需要回滚
            if sql[:7].rstrip().lower() in ["insert", "update", "delete", "replace"]:
                try:
                    db.ping(reconnect=True)
                    with db.cursor() as cursor:
                        # hack: resolv did'nt got data
                        if (isinstance(args, list) and len(args) > 0 and sql.find('touzhu') != -1):
                            print('checking dts')
                            for i in range(len(args)):
                                if ((args[i] == '' or args[i] == None)):
                                    print('init dt')
                                    args[i] = '0'
                        # 执行sql
                        if exe_type and exe_type == "MANY":
                            exe_result = cursor.executemany(sql, args)
                        else:
                            exe_result = cursor.execute(sql, args)
                        db.commit()
                        cursor.close()
                        return exe_result
                except Exception as e:
                    # 发生异常 回滚
                    db.rollback()
                    print('===============')
                    print(sql, e)
                    print(args)
                    print('===============')
            else:
                try:
                    db.ping(reconnect=True)
                    # 查询，不用做回滚
                    with db.cursor() as cursor:
                        # 执行sql
                        cursor.execute(sql, args)
                        result_query = cursor.fetchall()
                        db.commit()
                        cursor.close()
                        return result_query
                except Exception as e:
                    print('===============')
                    print(sql, e)
                    print(args)
                    print('===============')
                    pass

    @staticmethod
    def executeMany(sql, args):
        return DBUtils.execute(sql, args, "MANY")

    @staticmethod
    def executeOne(sql, args=None):
        return DBUtils.execute(sql, args, None)

    @staticmethod
    def queryNoDict(sql, args=None, ):
        if sql:
            sql = sql.lstrip()
            try:
                db.ping(reconnect=True)
                db.cursorclass = pymysql.cursors.Cursor
                with db.cursor() as cursor:
                    # 执行sql
                    cursor.execute(sql, args)
                    result_query = cursor.fetchall()
                    db.commit()
                    cursor.close()
                    return result_query
            except Exception as e:
                # 发生异常 回滚
                db.rollback()
                print('===============')
                print(sql, e)
                print(args)
                print('===============')


if __name__ == "__main__":
    result = DBUtils.queryNoDict("select * from test")
    print(list(result))
