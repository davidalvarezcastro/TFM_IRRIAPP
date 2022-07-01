import datetime


def get_now() -> datetime:
    return datetime.datetime.now()


def get_now_as_string() -> str:
    return get_now().strftime('%Y-%m-%d %H:%M:%S')
