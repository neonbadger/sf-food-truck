# -*- coding: utf-8 -*-

"""
The purpose of the classes is to instantiate a FoodTruck object with a JSON dictionary, and
we can use dot notation ('.'') or bracket notation ('[]') to access an attribute's value.

The classes are fairly basic at this point.
"""


class BaseClass(object):

    def __init__(self, data_dict):
        self.__dict__ = data_dict

    def __getitem__(self, key):
        return self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


class FoodTruck(BaseClass):

    def __init__(self, data_dict):
        super(FoodTruck, self).__init__(data_dict)

