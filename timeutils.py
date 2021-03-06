#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A module of helper functions for time-related operations.
"""


from datetime import datetime, timedelta


def get_datetime_now():
    """
    Returns the current local time as a datetime.datetime object.

    :return: datetime.datetime
    """

    now = datetime.now()
    return now


def format_24hr_time(datetime):
    """
    Returns a string displaying datetime in a 0-padded {24-Hour}:{Minute} format.

    This is the format used by the 'start24' and 'end24' fields in the Mobile Food Schedule dataset.

    :param datetime: datetime.datetime
    :return: str
    """

    string_24hr = datetime.strftime("%H:%M")
    return string_24hr


def format_string_literal(s):
    """
    Returns a string literal enclosed in matching single quotes (').

    This is needed to perform SoQL (Socrata Query Language) queries for the text datatype.

    Please see https://dev.socrata.com/docs/datatypes/text.html for details.

    :param s: str
    :return: str
    """

    return "\'{}\'".format(s)


def format_24hr_string_literal(datetime):
    """
    Returns a string representing the datetime in {24-Hour}:{Minute} format ready for SoQL operations.

    :param: datetime.datetime
    :return: str
    """

    string_24hr = format_24hr_time(datetime)
    return format_string_literal(string_24hr)


def convert_hour_to_seconds(hour):
    """
    Returns an int that converts hours into seconds.

    :param: int
    :return: int
    """

    return hour * 60 * 60


def get_time_delta(seconds):
    """
    Returns a datetime.timedelta object that represents the time difference in seconds.

    :param: int
    :return: datetime.timedelta
    """

    return timedelta(seconds=seconds)


def _get_future_datetime(datetime, time_delta):
    """
    Returns the future datetime from a known datetime given a datetime.timedelta.

    :param: datetime.datetime
    :param: datetime.timedelta
    :return: datetime.datetime
    """

    return datetime + time_delta


def get_future_datetime(datetime, hour):
    """
    Returns the future datetime from a known datetime given the hour difference.

    :param: datetime.datetime
    :param: int
    :return: datetime.datetime
    """

    seconds = convert_hour_to_seconds(hour)
    time_delta_in_seconds = get_time_delta(seconds)
    future_datetime = _get_future_datetime(datetime, time_delta_in_seconds)

    return future_datetime


def get_day_order(datetime):
    """
    Returns the day of the week as an integer, representing days in a week as follows:
    Sun - 0, Mon - 1, Tues - 2, Wed - 3, Thurs - 4, Fri - 5, and Sat - 6.

    This is the format used by 'dayorder' field in the Mobile Food Schedule dataset.

    For comparison, Python datetime.weekday() has the following mapping:
    Mon - 0, Tues - 1, Weds - 2, Thurs - 3, Fri - 4, Sat - 5, and Sun - 6.

    :param: datetime.datetime
    :return: int
    """

    dayorder = (datetime.weekday() + 1) % 7
    return dayorder



import unittest

class TestTimeUtils(unittest.TestCase):
    def test_get_day_order(self):
        today = datetime.today()
        today_dayorder = today.weekday()

        self.assertEqual(today_dayorder, 3)
        self.assertEqual(get_day_order(today), 4)

if __name__ == '__main__':
    unittest.main()


