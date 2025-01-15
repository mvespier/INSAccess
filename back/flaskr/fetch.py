import sys
import requests
from xml.etree import ElementTree
import re

CURRENT_YEAR = "2024"


def description_parsing():
    pass

def item_to_String():
    pass


def xml_to_list(url : str) -> list:
        
    response = requests.get(url)

    if response.status_code == 200: #request is successful
        xml_data = response.text  

        root = ElementTree.fromstring(xml_data)

    
        namespaces = {
            "ev": "http://purl.org/rss/1.0/modules/event/"
        }
        pattern_for_parsing_1 = r'(?<=<br/>).*'


        output =[]

        for item in root.findall("./channel/item"):
            title = item.find("title").text
            start_date = item.find("ev:startdate", namespaces).text
            end_date = item.find("ev:enddate", namespaces).text 
            description = item.find("description").text
            location = item.find("ev:location", namespaces).text

            



            description_without_beginning =re.findall(pattern_for_parsing_1, description )[0]
            #description_without_end = re.findall(pattern_for_parsing_2, description_without_beginning)[0][0]
            final_description = description_without_beginning.split(r'<br/>')[1:-2]
            
            


            output.append((title,start_date,end_date,final_description,location))
        
        return output


    else:
        print(f"Failed to fetch XML data. HTTP Status Code: {response.status_code}")
        return []




if __name__== "__main__" :
    if len(sys.argv)==4:
        list_of_depart = ["CGC", "EP", "GCU", "GM", "GPGR", "ITI", "MECA", "PERF-E", "PERF-II", "PERF-ISP", "PERF-NI"]
        list_of_period = ["day", "week", "month"]
        _, depart, year, period = sys.argv
        if ( (depart in list_of_depart) and (3 <= int(year) <= 5 ) and (period in list_of_period) ) :

            url = "http://agendas.insa-rouen.fr/rss/rss2.0.php?cal=" + CURRENT_YEAR+"-"+ depart + year + "&cpath=&rssview=" + period
            print("URL : " +url)
            out = xml_to_list(url)

            if (len(out) == 0) :
                print("ERROR : no match found")
            else : 
                for i in out:
                    print(i)

        else :
            print(f"ERROR : wrong arguments given : department = {list_of_depart}, 3 <= year <= 5, period = {list_of_period}" )

    else :
        print(f"ERROR : wrong number of arguments : must be 3 arguments, were given {len(sys.argv)-1}")
