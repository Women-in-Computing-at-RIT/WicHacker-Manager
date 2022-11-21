from datetime import datetime


def convertDatetimeToString(value):
    """
    Make sure Parser Input is string of type YYYY/MM/DD
    :param value:
    :return:
    """
    try:
        datetime.strptime(value, '%Y/%m/%d')  # try and convert input
        return value   # if no exception string is in correct format
    except Exception as err:
        raise ValueError(err)
