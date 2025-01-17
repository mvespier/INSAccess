import sys
import requests
from xml.etree import ElementTree
import re

def description_parsing(description):
    pattern_for_parsing = r'(?<=<br/>).*'

    description_without_beginning =re.findall(pattern_for_parsing, description )[0]
    final_description = description_without_beginning.split(r'<br/>')[1:-2]

    i= get_name_index(final_description)

    if i==None:
        return final_description,"none"
    return final_description [:i], final_description[i]

def get_name_index(list : list):
    for i in range(len(list)):
        if len(list[i].split(' ')) >1 :
            return i 
    

def item_to_string(item):

    return item.text if item != None else "None"


def xml_to_list(url : str) -> list:
        
    response = requests.get(url)

    if response.status_code == 200: #request is successful
        xml_data = response.text  

        root = ElementTree.fromstring(xml_data)

        namespaces = {
            "ev": "http://purl.org/rss/1.0/modules/event/"
        }
        output =[]

        for item in root.findall("./channel/item"):
            title = item_to_string(item.find("title"))
            start_date = item_to_string(item.find("ev:startdate", namespaces))
            end_date = item_to_string(item.find("ev:enddate", namespaces))
            description = item_to_string(item.find("description"))
            location = item_to_string(item.find("ev:location", namespaces))

            
            group_td, teacher =  description_parsing(description)

            output.append((title, start_date, end_date, group_td, teacher, location))
        
        return output
    else:
        print(f"Failed to fetch XML data. HTTP Status Code: {response.status_code}")
        return []

def get_calendar_data(current_year :int, department : str , year_depart : int, date : int, period :str) -> list :

    list_of_depart = ["CGC", "EP", "GCU", "GM", "GPGR", "ITI", "MECA", "PERF-E", "PERF-II", "PERF-ISP", "PERF-NI"]
    list_of_period = ["day", "week", "month"]

    if ( (department in list_of_depart) and (3 <= int(year_depart) <= 5 ) and (period in list_of_period) ) or (department =="STPI" and 1<= int(year_depart) <= 2) :

        url = "http://agendas.insa-rouen.fr/rss/rss2.0.php?cal=" + current_year+"-"+ department + year_depart + "&cpath=&rssview=" + period + "&getdate=" + date
        print("-"*150)
        print("URL : " + url)
        print("-"*150)
        out = xml_to_list(url)

        if (len(out) == 0) :
            print("ERROR : no match found")
        else : 
            for i in out:
                print(i)
            #return get_calendar_data
        print("-"*150)

    else :
        print(f"ERROR : wrong arguments given : department = {list_of_depart}, 3 <= year <= 5, period = {list_of_period}" )
    return 





if __name__== "__main__" :
    if len(sys.argv)==6:
        get_calendar_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    else :
        print(f"ERROR : wrong number of arguments : must be 5 arguments, were given {len(sys.argv)-1}")
