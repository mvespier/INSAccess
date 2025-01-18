import sys
import requests
from xml.etree import ElementTree
import re
import html

"""DEFAULT VALUE GETTER"""

def get_default_string() -> str:
    return "None"

def get_default_name() -> str:
    return "None"

def get_item_to_be_removed() -> list:
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
def xml_to_list(url : str, list_of_depart, depart_year) -> list:
        
    response = requests.get(url)

    if response.status_code == 200: #request is successful
        response.encoding = 'utf-8'
        xml_data = get_clean_xml(response.text)
        #print(xml_data)

        try:
            root = ElementTree.fromstring(xml_data)
        except ElementTree.ParseError as e:
            print(f"XML parsing error: {e}")
            return []

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

            
            group_td, teacher_list, group_depart =  description_parsing(description, list_of_depart, depart_year)

            output.append((date, start_hour, end_hour, locations, teacher_list, title, group_td, group_depart))
        
        return output
    else:
        print(f"Failed to fetch XML data. HTTP Status Code: {response.status_code}")
        return []


def get_calendar_data(current_year :str, department : str , depart_year : str, date : str, period :str) -> list :
    """
    get_calendar_data fetch the processed data from insa ALL PARAMETERS ARE STR.

    :param current_year: the current school year (i.e if 2024-2025 then = 2024)
    :param department: the department ("CGC", "EP", "GCU", "GM", "GPGR", "ITI", "MECA", "PERF-E", "PERF-II", "PERF-ISP", "PERF-NI" ...)
    :param depart_year: the year in the department (i.e ITI3 if third year and in ITI)
    :param date: the date you want to fetch (if you fetch for a week or month, give the month/week where the date is)
    :param period: the period you want (i.e day, week, month )

    :return: return a list of tuples (the days fetched)
    """ 


    list_of_depart = ["CGC", "EP", "GCU", "GM", "GPGR", "ITI", "MECA", "PERF-E", "PERF-II", "PERF-ISP", "PERF-NI"]
    list_of_period = ["day", "week", "month"]

    if ( (department in list_of_depart) and (3 <= int(depart_year) <= 5 ) and (period in list_of_period) ) or (department =="STPI" and 1<= int(depart_year) <= 2) :

        url = "http://agendas.insa-rouen.fr/rss/rss2.0.php?cal=" + current_year+ "-" + department + depart_year + "&cpath=&rssview=" + period + "&getdate=" + date
        out = xml_to_list(url, list_of_depart, depart_year)

        return url, out

    else :
        print(f"ERROR : wrong arguments given : department = {list_of_depart}, 3 <= year <= 5, period = {list_of_period}" )
        return []

def description_parsing(description, list_of_depart, depart_year):
    """I am fully aware that this part of the code isnt great because it is fitted"""
    """for very specific type of data but couldnt do better because of the chaos in the XML of Insa"""

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
    department_set = set(i+depart_year for i in list_of_depart)
    depart_in_desc, td_group_in_desc = [],[]
    for item in desc_item_list:
        if item in department_set:
            depart_in_desc.append(item)
        else:
            td_group_in_desc.append(item)


    #remove weird specific string that can appear in the td group thanks to INSA
    for i in range(len(td_group_in_desc)):
        if td_group_in_desc[i] in get_item_to_be_removed():
            td_group_in_desc.pop(i)


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


if __name__== "__main__" :
    if len(sys.argv)==6:
        url, out = get_calendar_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        print("-"*150)
        if (len(out) == 0) :
            print("Nothing found with those parameters")
        else : 
            print(f"Successfully fetched the data from : \n {url}")
            print("-"*150)
            for item in out :
                print(item) 

        print("-"*150) 
    else :
        print(f"ERROR : wrong number of arguments : must be 5 arguments, were given {len(sys.argv)-1}")
