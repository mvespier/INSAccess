from typing import List
import json



def get_query_tags(data_file_name : str, department :str, department_year :int, lang : list[str], ECAO :str) -> list[str] :

    with open(data_file_name) as f:
        data = json.load(f)
    
    if department == "STPI":
        depart_category = "STPI"
    else :
        depart_category = "DEPARTMENT"
        
    print(data[depart_category]["names"][department][str(department_year)])
    
    


    return []


if __name__ == "__main__" :
    get_query_tags("../../data/department.json", "ITI", 3, [""], "")
