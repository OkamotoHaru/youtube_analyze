from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# list型のindex()は存在しないをthrowされるのでラップして-1を返す
def index(list, value):
    try:
        return list.index(value)
    except Exception as e:
        return -1

# 前日の最終時刻を取得する
def yesterdayLastDate():
    dt_now = datetime.now()
    last = dt_now - timedelta(days=1)
    formatted = last.strftime('%Y-%m-%dT23:59:59Z')
    return formatted

# １年前の開始時刻を取得する
def lastYear():
    dt_now = datetime.now()
    last = dt_now - relativedelta(years=1)
    formatted = last.strftime('%Y-%m-%dT00:00:00Z')
    return formatted