from datetime import datetime, timezone, timedelta, date
import time

"""
timeStr = 'Fri, 19 Aug 2022 07:30:02 +0000'
emailLocalTime = datetime.strptime(timeStr, "%a, %d %b %Y %H:%M:%S %z")
d = emailLocalTime.replace(tzinfo=timezone.utc)  # Convert it to an aware datetime object in UTC time.
d = d.astimezone()  # Convert it to your local timezone (still aware)
print(d.strftime("%Y-%m-%d %H:%M:%S"))
"""

local_format_str = '%Y-%m-%d %H:%M:%S'


def now_str(format_str='%Y-%m-%d %H:%M:%S'):
    # 获取当前时间
    # current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    now = datetime.now()
    # 转换为字符串
    return now.strftime(format_str)


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """

    now = datetime.now()
    diff = 0
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"


def get_time_from_str(time_str):
    emailLocalTime = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.000Z")
    d = emailLocalTime.replace(tzinfo=timezone.utc)  # Convert it to an aware datetime object in UTC time.
    d = d.astimezone()  # Convert it to your local timezone (still aware)
    # print(d.strftime("%Y-%m-%d %H:%M:%S"))
    return d


def get_special_to_local(time_str: str = None, format_str='%Y-%m-%d#%H:%M:%S'):
    d = get_time_from_str(time_str)
    return d.strftime(format_str)


def get_utc_time_str(formatStr="%Y-%m-%dT%H:%M:%S.000Z"):
    return str(datetime.utcnow().strftime(formatStr))


def get_time_ago(minutes=10, formatStr="%Y-%m-%dT%H:%M:%S.000Z"):
    return datetime.strftime(datetime.now() + timedelta(minutes=minutes), formatStr)


def time_diff_now(time_val, original_format=local_format_str, get_type='seconds', precision=2):
    """
    返回参数与当前时间相隔的  秒数
    """
    if time_val is None or time_val == '':
        return 0
    now = datetime.now()
    diff = 0
    if type(time_val) is int or type(time_val) is float:
        return round(time.time() - time_val, precision)
    elif isinstance(time_val, datetime):
        diff = now - time_val
    elif isinstance(time_val, str):
        getTime = datetime.strptime(time_val, original_format)
        diff = now - getTime
    if get_type == 'days':
        return diff.days
    return diff.total_seconds()


def str_to_timestamp(timeStr):
    import time
    # print(time.strptime(timeStr, local_format_str).)
    return int(datetime.strptime(timeStr, local_format_str).timestamp() * 1000)


def time_diff_time(date_string, days=2, timeStrFormat="%Y-%m-%d %H:%M:%S"):
    # 获取当前日期时间
    now = datetime.now()
    # 计算两天前的日期时间
    days_ago = now - timedelta(days=days)
    diff = 0
    if type(date_string) is int:
        diff = days_ago - datetime.fromtimestamp(date_string)
    elif isinstance(date_string, datetime):
        diff = days_ago - date_string
    elif isinstance(date_string, str):
        getTime = datetime.strptime(date_string, timeStrFormat)
        diff = days_ago - getTime
    return diff.total_seconds()


def timestamp_to_date_str(timestamp, dateFormat='%Y-%m-%d %H:%M:%S'):
    if timestamp == 0:
        return 0
    if timestamp > 10 ** 12:
        timestamp /= 1000
    # 将时间戳转换为datetime对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 将datetime对象格式化为字符串
    date_string = dt_object.strftime(dateFormat)
    return date_string


def get_previous_date(days=1):
    # 获取当前日期
    today = date.today()
    # 计算前一天的日期
    previous_date = today - timedelta(days=days)
    # yesterday.strftime('%Y-%m-%d')
    return previous_date


def get_weekday(next_days=3):
    # 获取当前日期
    now = datetime.now()

    # 获取3天后的日期
    three_days_later = now + timedelta(days=next_days)

    # 获取3天后是星期几
    weekday = three_days_later.weekday()
    is_next_weekday = '下'
    if now.isocalendar()[1] == three_days_later.isocalendar()[1]:
        is_next_weekday = '这'
    # 将整数转换为星期几
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
    return is_next_weekday + weekdays[weekday]


if __name__ == '__main__':
    print(get_time_from_str('2022-09-16T17:48:06.000Z').strftime("%Y-%m-%d#%H:%M:%S"))
    abc = time_diff_now('2024-06-01 08:00:00', get_type='days')
    print(f'相隔天数{abc}')
    # print(len('2022-11-06_11:04:15_713955'))
    # get_local_str()
    print(str_to_timestamp('2022-11-05 14:00:00'))
    print("####")
    print(time_diff_time("2024-02-24 12:25:45"))
    print(datetime.now())
    print(f"今天{now_str('%Y-%m-%d 00:00:00')}")
    print(get_weekday(next_days=4))
    print(get_previous_date(1).strftime('%Y-%m-%d 00:00:00'))

    print(timestamp_to_date_str(1719369710000))
    print(f'时间差异： {time_diff_now(1730965391)}')
