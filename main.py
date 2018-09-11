#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A command line program that prints to the console the food truck that are open
at the time the program is run.
"""


import os
import requests
import time

from printutils import *
from queryutils import build_payload
from timeutils import get_datetime_now, format_24hr_string_literal, get_day_order


FOODTRUCK_DATASET_BASE_URL = "https://data.sfgov.org/resource/bbb8-hzi6.json"
APP_TOKEN = os.environ.get("APP_TOKEN", None)


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
                               timeout=10)

        # throw excpetion when request does not return a 2XX status code
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print_http_error(e)
        return -1

    return response


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

    return user_input != None and user_input.lower() != "e"


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

    data_fields = ["applicant", "location"]
    sort_order = data_fields[0]

    page_limit = 10
    page_index = 0

    first_load = True

    retries = 0
    max_retries = 3
    retrying = False

    print_opening(now_datetime)

    while retries < max_retries:

        # Skip prompt until first display or during automatic retries
        if not (first_load or retrying):
            user_input = prompt_for_user_input()


        # Make server call if:
        # (1) first call, (2) user continues, or (3) automatic retries
        if first_load or go_to_next_page(user_input) or retrying:

            response = fetch_data_in_batches(data_fields,
                                             today_day_order,
                                             current_time,
                                             sort_order,
                                             page_limit,
                                             page_index)

            # Unsuccessful HTTP request: retry after 2 seconds
            if response == -1:
                retries += 1
                retrying = True

                if retries == max_retries:
                    print_end(error=True)
                    break

                time.sleep(2)
                continue

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

        # User cancel case
        else:
            print_end(user_cancel=True)
            break


if __name__ == '__main__':
    main()