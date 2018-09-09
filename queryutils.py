# -*- coding: utf-8 -*-

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
