#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A module of helper functions to build URL
"""


import urllib
import urlparse


def build_url(base_url, path, **args_dict):
    """
    Returns a list in the structure of urlparse.ParseResult.

    :param: string
    :param: string
    :param: dict
    """

    url_parts = list(urlparse.urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urllib.urlencode(args_dict)

    return urlparse.urlunparse(url_parts)
