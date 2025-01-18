import sys
import requests
from xml.etree import ElementTree
import re
import html

def description_parsing(description, list_of_depart, depart_year):
    pattern_for_parsing = r'(?<=<br/>).*'

    description_without_beginning =re.findall(pattern_for_parsing, description )[0]
    final_description = description_without_beginning.split(r'<br/>')[1:-2]

    i= get_name_index(final_description)

    name = final_description.pop(i) if i!=None else 'none'


    department_set = set(i+depart_year for i in list_of_depart)

    depart_in_desc, td_group_in_desc = [], []
    for item in final_description:
        if item in department_set:
            depart_in_desc.append(item)
        else:
            td_group_in_desc.append(item)

    return [item for item in td_group_in_desc if item != 'examens'], name, depart_in_desc

def get_name_index(list : list):
    for i in range(len(list)):
        if len(list[i].split(' ')) >1 :
            return i 


def item_to_string(item):

    return item.text if item != None else "None"



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
            location = item_to_string(item.find("ev:location", namespaces))

            
            group_td, teacher, group_depart =  description_parsing(description, list_of_depart, depart_year)

            output.append((date, start_hour, end_hour, location, teacher, title, group_td, group_depart))
        
        return output
    else:
        print(f"Failed to fetch XML data. HTTP Status Code: {response.status_code}")
        return []

def get_calendar_data(current_year :int, department : str , depart_year : int, date : int, period :str) -> list :

    list_of_depart = ["CGC", "EP", "GCU", "GM", "GPGR", "ITI", "MECA", "PERF-E", "PERF-II", "PERF-ISP", "PERF-NI"]
    list_of_period = ["day", "week", "month"]

    if ( (department in list_of_depart) and (3 <= int(depart_year) <= 5 ) and (period in list_of_period) ) or (department =="STPI" and 1<= int(depart_year) <= 2) :

        url = "http://agendas.insa-rouen.fr/rss/rss2.0.php?cal=" + current_year+"-"+ department + depart_year + "&cpath=&rssview=" + period + "&getdate=" + date
        print("-"*150)
        print("URL : " + url)
        print("-"*150)
        out = xml_to_list(url, list_of_depart, depart_year)

        if (len(out) == 0) :
            print("Nothing found with those parameters")
            return []
        else : 
            for i in out:
                print(i)
            return out
        print("-"*150) 


    else :
        print(f"ERROR : wrong arguments given : department = {list_of_depart}, 3 <= year <= 5, period = {list_of_period}" )
        return []





if __name__== "__main__" :
    if len(sys.argv)==6:
        out = get_calendar_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        
    else :
        print(f"ERROR : wrong number of arguments : must be 5 arguments, were given {len(sys.argv)-1}")