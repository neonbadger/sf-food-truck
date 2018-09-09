#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A module of helper functions for time-related operations.
"""


from datetime import datetime


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

