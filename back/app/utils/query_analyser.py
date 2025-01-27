"""
Module Name: query_analyser.py

Description:
    The script for interpreting the given arguments
    into tags that can be used in the database

Author:
    Raphael Senellart

Date Created:
    January 25, 2025

Version:
    1.0.0

License:
    No License

Usage:
    NOT DONE YET

Dependencies:


Notes:
    This tool is specialized for the agenda.insa-rouen.fr
    website, but some methods are generic and can be implemented
    else where.

"""
from typing import List
import json


def cartesian_product(list_1 : List[str], list_2 : List[str]) -> List:
    """Does the concatenation of the cartesian product between 2 list of String

    Keyword arguments:
    l1 -- the first list (the elements within are first in the finals string)
    l2 -- the second list (the elements within are last in the finals string)
    Return: list of concatenated string
    """

    return [ a + b for a in list_1 for b in list_2]

def get_tags_from_dict(dict_given, *keys):
    """return the tags created by navigating the given dict
        (used for creating the corresponding tags)
    for the sql database

    Keyword arguments:
    :param dict_given: -- the dict navigated
    :param *keys: -- the keyword used to select specific tags within the dict
    Return: a set of tags
    """

    temp_dict = dict_given
    tags = set()
    tags_beginning = []
    for k in keys:

        if "default_tags" in temp_dict:
            for item in temp_dict["default_tags"]:
                tags.add(item)

        if "tags_starts_with" in temp_dict:
            if len(tags_beginning) > 0 :
                raise ValueError("tags_starts_with found twice in json")
            tags_beginning = temp_dict["tags_starts_with"]

        if "tags+" in temp_dict:
            temp = []
            for item in cartesian_product(tags_beginning,temp_dict["tags+"]):
                temp.append(item)
            tags_beginning = temp.copy()


        if k in temp_dict:
            if isinstance(temp_dict[k], dict):
                temp_dict = temp_dict[k]
            else :
                for item in cartesian_product(tags_beginning,temp_dict[k]):
                    tags.add(item)
                return tags

    raise ValueError("no final tag part")


def get_query_tags(data_file_name : str, department :str,\
                    department_year :int, *specialization) -> list[str] :
    """return the entire tags needed for fetching the database
    according to given arguments

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    with open(data_file_name, encoding='utf8') as file:
        data = json.load(file)

    tags = set()
    temp_tags = set()
    base_args = [department, department_year]

    for finals_args in specialization:
        try :
            full_args = base_args+finals_args
            temp_tags =  get_tags_from_dict(data, *full_args)
        except ValueError as err:
            print(f"Error in get_tags_from_dict : {err}")
        tags.update(temp_tags)

    print(tags)
    return tags


if __name__ == "__main__" :
    get_query_tags("../../data/department.json", "ITI", "3", ["LANGUE", "ANGLAIS","1"],["LANGUE", "ALLEMAND", "2"],["TD", "2"])

