#!/usr/bin/env python
# encoding: utf-8

import os
import requests
import time

from datetime import datetime
from FoodTruck import FoodTruck

FOODTRUCK_DATASET_BASE_URL = "https://data.sfgov.org/resource/bbb8-hzi6.json"
APP_TOKEN = os.environ.get("app_token", None)

### TIME UTILS ###
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

    See https://dev.socrata.com/docs/datatypes/text.html for details.

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


### QUERY PARAMS ###
# https://dev.socrata.com/docs/queries/
def build_select_clause(data_fields):
    """
    Returns a comma-separated string to retrieve fields for the $select URL parameter.

    :param data_fields: list
    """

    return ",".join(data_fields)


def build_where_clause(day_order, time_string):
    """
    Returns a string to filter results for the $where URL parameter -- specifically,
    businesses that are open on a given day within a given time range.

    :param day_order: int
    :param time_string: str
    :return: str
    """

    return "dayorder = {} AND {} > start24 AND {} < end24".format(day_order,
                                                                  time_string,
                                                                  time_string)


def build_limit_clause(page_limit):
    """
    Returns a string for $limit URL parameter to denote how many records to be returned.

    To achieve pagination, $offset is often used in conjunction with $limit.

    :param page_limit: int
    :return: string
    """

    return str(page_limit)


def build_offset_clause(page_limit, page_index=0):
    """
    Returns a string for the $offset URL parameter to specify the starting position in the
    dataset to retrieve records from. Note that page_index is 0-based.

    To achieve pagination, $offset is often used in conjunction with $limit.

    For example, if page_limit is 10 and page_index is at 3 ("4th page" from the 0 index),
    offset begins at record number 30 (page_limit * page_index).

    :param page_limit: int
    :param page_index: int, defaults to 0 (beginning of the dataset)
    :return: str
    """

    return str(page_limit * page_index)


def build_order_clause(sort_field, order="ASC"):
    """
    Returns a string for the $order URL parameter.

    :param sort_field: str
    :param order: str, ASC or DESC - defaults to ASC
    :return: str
    """

    return "{} {}".format(sort_field, order)


def build_payload(data_fields,
                  day_order,
                  time_string,
                  sort_order,
                  page_limit,
                  page_index):
    """
    Returns a dictionary that maps URL parameters to respective query values.

    :param data_fields: list
    :param day_order: int
    :param time_string: str
    :param sort_order: str
    :param page_limit: int
    :param page_index: int
    :return: dictionary
    """

    payload = {
        "$select" : build_select_clause(data_fields),
        "$where"  : build_where_clause(day_order, time_string),
        "$order"  : build_order_clause(sort_order),
        "$limit"  : build_limit_clause(page_limit),
        "$offset" : build_offset_clause(page_limit, page_index),
    }

    return payload


def fetch_data_in_batches(data_fields,
                          day_order,
                          time_string,
                          sort_order,
                          page_limit,
                          page_index):
    """
    Returns a requests.Response object that contains response to a successful HTTP request,
    or -1 if the request is unsuccessful.

    Data can be returned in batches (paging) by using the $limit and $offset URL parameters
    in conjunction.

    :param data_fields: list
    :param day_order: int
    :param time_string: str
    :param sort_order: str
    :param page_limit: int
    :param offset: int
    :return: requests.Response if request is successful, or -1 if not
    """

    header = {'X-Auth-Token': APP_TOKEN}

    payload = build_payload(data_fields,
                            day_order,
                            time_string,
                            sort_order,
                            page_limit,
                            page_index)

    try:
        session = requests.session()
        response = session.get(FOODTRUCK_DATASET_BASE_URL,
                               headers=header,
                               params=payload,
                               timeout=5)

        # throw excpetion when request does not return 2XX
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print "HTTP error {}".format(e.message)
        return -1

    except requests.exceptions.ConnectionError as e:
        print "Connection error {}".format(e.message)
        return -1

    except requests.exceptions.Timeout as e:
        print "Timeout error {}".format(e.message)
        return -1

    except requests.exceptions.RequestException as e:
        print "Oops: Something went wrong {}".format(e.message)
        return -1

    return response


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


def prompt_for_user_input():
    """
    Returns a string of user input in response to a command line prompt.

    :return: string
    """
    prompt_string = "\nGet the next 10 results? Type letter 'e' to exit, or any other key to continue.\n"
    user_input = raw_input(prompt_string)

    return user_input


def go_to_next_page(user_input):
    """
    Returns False if user input equals letter 'e' or 'E', or True for any other input.

    :param user_input: str
    :return: bool
    """

    return user_input.lower() != "e"


def is_empty(json_response):
    """
    Returns True if the JSON response is an empty list, False if the response contains an item(s).

    :param: list
    :return: boolean
    """

    return len(json_response) == 0


def is_end(json_response, page_limit):
    """
    Returns True if the number of items in the JSON response is less than the page limit.

    :param json_response: list
    :param page_limit: int
    """

    return len(json_response) < page_limit


def main():

    now_datetime = get_datetime_now()
    current_time = format_24hr_string_literal(now_datetime)

    today_day_order = get_day_order(now_datetime)

    data_fields = ["applicant", "location", "starttime", "endtime", "start24", "end24", "dayofweekstr"]
    sort_order = data_fields[0]

    page_limit = 10
    page_index = 0

    first_load = True

    retries = 0
    max_retries = 3
    retrying = False

    print_opening(now_datetime)

    while retries < max_retries:

        if not (first_load or retrying):
            user_input = prompt_for_user_input()

        if first_load or go_to_next_page(user_input) or retrying:

            response = fetch_data_in_batches(data_fields,
                                             today_day_order,
                                             current_time,
                                             sort_order,
                                             page_limit,
                                             page_index)

            # HTTP struggle land: allow retries
            if response == -1:
                retries += 1
                retrying = True

                if retries == max_retries:
                    print_end(error=True)
                    break

                time.sleep(2)
                continue

            # HTTP success land
            parsed_response = response.json()

            if retrying:
                retries = 0
                retrying = False

            if first_load:
                print_food_truck_header()
                first_load = False

            if not is_empty(parsed_response):
                print_all_food_trucks(parsed_response)
                page_index += 1

            if is_empty(parsed_response) or is_end(parsed_response, page_limit):
                print_end()
                break

        else:
            print_end(user_terminate=True)
            break

if __name__ == '__main__':
    main()