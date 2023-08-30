import datetime


def sanitize_dates(start, end):

    if start is None:
        start = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    if end is None:
        end = start

    return start, end
