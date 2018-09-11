#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A module of helper functions to print to the command line.
"""


from foodtruckclass import FoodTruck
from requests.exceptions import ConnectionError, HTTPError, Timeout, RequestException


def print_all_food_trucks(response_json):
    """
    Iterate through the JSON response list and print each item in the list.

    :param response_json: list
    """

    for item_json in response_json:
        print_food_truck(item_json)


def print_food_truck(food_truck_dict):
    """
    Print the name and location of a FoodTruck object.

    :param food_truck_dict: dict
    """

    food_truck = FoodTruck(food_truck_dict)
    name = food_truck.applicant
    location = food_truck.location

    print_two_columns(name, location)


def print_two_columns(s1, s2):
    """
    Print two left-aligned columns of fixed width.

    :param s1: str
    :param s2: str
    """

    print "{:<80} {:<10}".format(s1, s2)


def print_opening(datetime):
    """
    Print summary and instructions of the command line program.

    Time is displayed in a more readable format like this:'09/08/2018 Sat 05:00 PM'.

    :param: datetime.datetime
    """

    time_string = datetime.strftime("%m/%d/%Y %a %I:%M %p")

    print "#####################################################################"
    print "*** SF food trucks open currently at {} ***".format(time_string)
    print "*** You will view 10 results at a time, ordered by the food truck's name alphabetically. ***"
    print "*** You can type any key to view 10 results as a time. Or type letter 'e' case-insensitive to exit. ***"
    print ""
    print ""


def print_food_truck_header():
    """
    Print headers for the food truck data.
    """

    print_two_columns("NAME", "ADDRESS")


def print_end(error=False, user_cancel=False):
    """
    Prints different messages to signal end of the command line program.

    :param error: bool, default to False
    :param user_terminate: bool, default to True
    """

    if error:
        print "\nMax retries exceeded. Exiting the program... Bye!\n"
    elif user_cancel:
        print "\nYou ended this program. Thanks for visiting! Bye!\n"
    else:
        print "#### END ####\n"


def print_http_error(e):
    """
    Print an error message for different HTTP exceptions.

    requests.exceptions.RequestException is the base class and is the catch all exception type.

    :param e: requests.exceptions
    """

    message_body = ""

    if isinstance(e, HTTPError):
        messages_body = "HTTP error {}\n".format(e.message)

    elif isinstance(e, ConnectionError):
        messages_body = "Connection error {}\n".format(e.message)

    elif isinstance(e, Timeout):
        messages_body  = "Timeout error {}\n".format(e.message)

    elif isinstance(e, RequestException):
        messages_body = "Oops: Something went wrong {}\n".format(e.message)

    print messages_body

