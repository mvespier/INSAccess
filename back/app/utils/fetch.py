"""
Module Name: fetch.py

Description:
    The script for fetching and parsing the raw 
    data from the calendar of insa rouen.

Author:
    Raphael Senellart

Date Created:
    January 25, 2025

Version:
    1.0.0

License:
    No License

Usage:
    Can be ran using :
    python3 fetch.py current_year department depart_year date period
    or if you want to fetch the entire year :
    python3 fetch.py year_of_start department depart_year

Dependencies:
    

Notes:
    This tool is specialized for the agenda.insa-rouen.fr
    website, but some methods are generic and can be implemented
    else where.

"""
from xml.etree import ElementTree
import sys
import re
import html
import itertools
import requests

ERROR_FAILED_TO_PARSE = 666
ERROR_WRONG_ARG = 42
SUCESS_CODE = 0


"""DEFAULT VALUE GETTER"""

def get_default_string() -> str:
    """return the constant for the default string"""
    return ""

def get_default_name() -> str:
    """return the constant for the default name"""
    return ""

def get_item_to_be_removed() -> list:
    """ return the constant list that should be removed
        from the list of groups
        (they are weird tags that the secretary sometime put)"""
    return ['examens']


""" XML ENCODING ISSUE CLEANING """

def replace_entities(content, replacements):
    for entity, replacement in replacements.items():
        content = content.replace(entity, replacement)
    return content

def get_clean_xml(xml_data :str ) -> str :
    entity_replacements = {
    '&eacute;': 'é',
    '&Eacute;': 'É',
    '&agrave;': 'à',
    '&Agrave;': 'À',
    '&ocirc;': 'ô',
    '&ucirc;': 'û',
    '&icirc;': 'î',
    '&ccedil;': 'ç',
    '&nbsp;': ' ',
    '&': '&amp;'
    }

    return replace_entities(xml_data, entity_replacements)


def remove_invalid_chars(content):
    # Valid XML characters (see XML spec)
    valid_xml_characters = (
        r"[\u0009\u000A\u000D\u0020-\uD7FF\uE000-\uFFFD\u10000-\u10FFFF]"
    )
    return re.sub(f"[^{valid_xml_characters}]+", "", content)


def replace_entities(content, replacements):
    for entity, replacement in replacements.items():
        content = content.replace(entity, replacement)

    content = html.unescape(content)
    content = remove_invalid_chars(content)

    return content

""" MAIN FUNCTIONS """
def xml_to_list(url : str, depart_list, depart_year) -> list:
    global ERROR_FAILED_TO_PARSE
    response = requests.get(url)

    if response.status_code == 200: #request is successful
        response.encoding = 'utf-8'
        xml_data = get_clean_xml(response.text)
        #print(xml_data)

        try:
            root = ElementTree.fromstring(xml_data)
        except ElementTree.ParseError as e:
            print(f"XML parsing error: {e}")
            return ERROR_FAILED_TO_PARSE, []

        root = ElementTree.fromstring(xml_data)

        namespaces = {
            "ev": "http://purl.org/rss/1.0/modules/event/"
        }
        output =[]

        for item in root.findall("./channel/item"):
            title = item_to_string(item.find("title"))
            date, start_hour = item_to_string(item.find("ev:startdate", namespaces)).split('T')
            _, end_hour = item_to_string(item.find("ev:enddate", namespaces)).split('T')
            description = item_to_string(item.find("description"))
            locations = item_to_string(item.find("ev:location", namespaces)).split('%2C')

            title = title_parsing(title)


            group_td, teacher_list, group_depart =  description_parsing(description, depart_list)

            output.append((date, start_hour, end_hour, title, locations,\
                            teacher_list, group_td, group_depart))

        return output
    else:
        print(f"Failed to fetch XML data. HTTP Status Code: {response.status_code}")
        return []


def get_calendar_data(current_year :str, department : str ,\
                       depart_year : str, date : str, period :str) -> list :
    """
    get_calendar_data fetch the processed data from insa ALL PARAMETERS ARE STR.

    :param current_year: the current school year
    (i.e if 2024-2025 then = 2024)

    :param department: the department
    ("CGC", "EP", "GCU", "GM", "GPGR", "ITI", "MECA",
    "PERF-E", "PERF-II", "PERF-ISP", "PERF-NI" ...)

    :param depart_year: the year in the department
    (i.e ITI3 if third year and in ITI)

    :param date: the date you want to fetch
    (if you fetch for a week or month, give the month/week where the date is)

    :param period: the period you want
    (i.e day, week, month )

    :return: return a list of tuples (the days fetched)
    """
    global ERROR_WRONG_ARG

    depart_list = ["CGC", "EP", "GCU", "GM", "GPGR", "ITI",\
                    "MECA", "PERF-E", "PERF-II", "PERF-ISP", "PERF-NI"]
    list_of_period = ["day", "week", "month"]

    if ( (department in depart_list) and (3 <= int(depart_year) <= 5 )\
         and (period in list_of_period) ) or (department =="STPI" and 1<= int(depart_year) <= 2) :

        url = "http://agendas.insa-rouen.fr/rss/rss2.0.php?cal=" + current_year\
            + "-" + department + depart_year + "&cpath=&rssview=" + period + "&getdate=" + date
        out = xml_to_list(url, depart_list, depart_year)

        return SUCESS_CODE, out

    else :
        print(f"ERROR : wrong arguments given : department = {depart_list},\
               3 <= year <= 5, period = {list_of_period}" )
        return ERROR_WRONG_ARG, []

def title_parsing(title):
    class_name = title.split(': ')[1]
    class_name = class_name.replace('-', ' ')
    return class_name


def description_parsing(description, depart_list):
    """I am fully aware that this part of the code isnt great because it is fitted
    for very specific type of data but couldnt do better
    because of the chaos in the XML of Insa"""

    #pre-treatement of the description
    pattern_for_parsing = r'(?<=<br/>).*'
    try :
        desc_string = re.findall(pattern_for_parsing, description )[0]
    except IndexError as e:
        print(f"List Index error: {e}")
        return [],get_default_name() ,[]

    desc_item_list = desc_string.split(r'<br/>')[1:-2] # 1 to -2 because the last and first are empty and the -2 is just the date of submission


    #get and remove the name if there is one
    list_of_indexes = get_name_indexes(desc_item_list)
    name_list, desc_item_list = pop_multiple_element(desc_item_list, list_of_indexes)


    # separate the department and tdgroup from the description into 2 list
    depart_years =['3', '4', '5']
    department_set = set(map(''.join, itertools.product(depart_list,depart_years)))
    department_set.add('STPI1')
    department_set.add('STPI2')

    depart_in_desc, td_group_in_desc = [],[]
    for item in desc_item_list:
        if item in department_set:
            depart_in_desc.append(item)
        else:
            td_group_in_desc.append(item)


    #remove weird specific string that can appear in the td group thanks to INSA
    list_of_indexes_filter=[]
    for i in range(len(td_group_in_desc)):
        if td_group_in_desc[i] in get_item_to_be_removed():
            list_of_indexes_filter.append(i)
    _, td_group_in_desc = pop_multiple_element(td_group_in_desc,list_of_indexes_filter)


    return td_group_in_desc, name_list, depart_in_desc

def get_name_indexes(list : list):
    list_of_indexes=[]
    for i in range(len(list)):
        if len(list[i].split(' ')) >1 :
            list_of_indexes.append(i)
    return list_of_indexes

def pop_multiple_element(list, list_of_indexes):
    deleted_element = [list[i] for i in list_of_indexes]
    filtered_list = [list[i] for i in range(len(list)) if i not in list_of_indexes]
    return deleted_element, filtered_list

def item_to_string(item):
    return item.text if item != None else get_default_string()


def return_unique_td(out):
    unique = set()
    for item in out :
        for element in item[6]:
            unique.add(element)
    for i in sorted(unique):
        print(i)

def return_unique_date(out):
    unique = set()
    for item in out :
        unique.add(item[0][:-3])
    for i in sorted(unique,reverse=True):
        print(i)


def return_all(out):
    for item in out :
        print(item)

def fetch_entire_year(year_of_start, department, depart_year):
    total_list=[]
    for i in {"08", "09", "10", "11", "12"}:
        date = year_of_start + i + "01"
        total_list = total_list + get_calendar_data(year_of_start,\
                                                     department, depart_year, date, "month")[1]
    for i in {"01", "02", "03", "04", "05", "06", "07","08"}:
        date = str(int(year_of_start)+1) + i + "01"
        total_list = total_list + get_calendar_data(year_of_start,\
                                                     department, depart_year, date, "month")[1]
    return total_list

if __name__== "__main__" :
    if len(sys.argv)==6:
        error_code, out = get_calendar_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        # print("-"*150)
        if (len(out) == 0) :
            print("Nothing found with those parameters")
        else :
            # print(f"Error code : {error_code}")
            # print("-"*150)
            return_all(out)

        # print("-"*150)
    elif len(sys.argv)==4:
        out = fetch_entire_year(sys.argv[1], sys.argv[2], sys.argv[3])
        return_unique_td(out)
    else:
        print(f"ERROR : wrong number of arguments : must be 5 arguments, were given {len(sys.argv)-1}")
