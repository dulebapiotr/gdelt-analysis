from datetime import datetime

_sql_string = '%Y%m%d'
_js_string = '%Y-%m-%d'


def sql_date_to_datetime(sql_date: int) -> datetime:
    return datetime.strptime(str(sql_date), _sql_string)


def js_date_to_datetime(js_date: str) -> datetime:
    return datetime.strptime(js_date, _js_string)


def datetime_to_sql_date(date) -> int:
    return int(date.strftime(_sql_string))


def datetime_to_js_date(date: datetime) -> str:
    return date.strftime(_js_string)


def js_date_to_sql_date(js_date: str) -> int:
    datetime_date = js_date_to_datetime(js_date)
    date = datetime_to_sql_date(datetime_date)
    return int(date)


def sql_date_to_js_date(sql_date: int) -> str:
    datetime_date = sql_date_to_datetime(sql_date)
    return datetime_to_js_date(datetime_date)
