import datetime


from globals import DATE_FORMAT


def get_now() -> datetime:
    return datetime.datetime.now()


def get_now_as_string() -> str:
    return get_now().strftime(DATE_FORMAT)


def get_datetime_from_string(date: str) -> datetime.datetime:
    return datetime.datetime.strptime(date, DATE_FORMAT)
