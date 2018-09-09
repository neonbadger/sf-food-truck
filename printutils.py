# -*- coding: utf-8 -*-

from foodtruck import FoodTruck


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

    # print_two_columns(name, location)

    starttime = food_truck.starttime
    endtime = food_truck.endtime
    start24 = food_truck.start24
    end24 = food_truck.end24
    dayofweekstr = food_truck.dayofweekstr

    print name, location, starttime, start24, endtime, end24, dayofweekstr


def print_two_columns(s1, s2):
    """
    Print two left-aligned, fixed-sized columns.

    :param s1: string
    :param s2: string
    """

    print "{:<80} {:<10}".format(s1, s2)


def print_opening(datetime):
    """
    Print summary and instructions of the program.

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


def print_end(error=False, user_terminate=False):
    """
    Prints different messages to signal end of the program.

    :param error: boolean, default to False
    :param user_terminate: boolean, default to True
    """

    if error:
        print "\nMax retries exceeded. Exiting the program... Bye!\n"
    elif user_terminate:
        print "\nYou ended this program. Thanks for visiting! Bye!\n"
    else:
        print "#### END ####\n"

