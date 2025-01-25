from typing import List
import json


def cartesian_product(l1 : List[str], l2 : List[str]) -> List:
    return [ a + b for a in l1 for b in l2]

def get_tags_from_dict(dict_given, *keys):
    temp_dict = dict_given
    tags = set()
    tags_beginning = []
    for k in keys:
        if "default_tags" in temp_dict:
            for item in temp_dict["default_tags"]:
                tags.add(item)

        if "tags_starts_with" in temp_dict:
            if len(tags_beginning) > 0 :
                raise Exception("tags_starts_with found twice in json")
            tags_beginning = temp_dict["tags_starts_with"]
        
        if "tags+" in temp_dict:
            temp = []
            for item in cartesian_product(tags_beginning,temp_dict["tags+"]):
                temp.append(item)
            tags_beginning = temp.copy()
            

        if k in temp_dict:
            if type(temp_dict[k]) is dict:
                temp_dict = temp_dict[k]
            else :
                for item in cartesian_product(tags_beginning,temp_dict[k]):
                    tags.add(item)
                return tags
            
    raise Exception("no final tag part")


def get_query_tags(data_file_name : str, department :str, department_year :int, lang : list[str], ECAO :str) -> list[str] :

    with open(data_file_name) as f:
        data = json.load(f)
    
    tags = set()
    temp_tags = set()
    try : 
        toto = ["ITI", "3", "LANGUE","ANGLAIS", "1"]
        temp_tags =  get_tags_from_dict(data, *toto)
    except Exception as er:
        print(f"Error in get_tags_from_dict : {er}")
    for item in temp_tags:

        tags.add(item)
    print(tags)


    


    return []


if __name__ == "__main__" :
    get_query_tags("../../data/department.json", "ITI", 3, [""], "")
