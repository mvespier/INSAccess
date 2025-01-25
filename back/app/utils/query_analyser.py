from typing import List
import json
import itertools


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
                return -1, set();
            tags_beginning = temp_dict["tags_starts_with"]
        
        if "tags+" in temp_dict:
            temp = []
            for item in itertools.product(tags_beginning,temp_dict["tags+"]):
                temp.append(item[0] + item[1])
            tags_beginning = temp.copy()
            

        if k in temp_dict:
            if type(temp_dict[k]) is dict:
                temp_dict = temp_dict[k]
            else :
                for item in itertools.product(tags_beginning,temp_dict[k]):
                    tags.add(item[0] +item[1])
                return 0, tags
    return 0, set()


def get_query_tags(data_file_name : str, department :str, department_year :int, lang : list[str], ECAO :str) -> list[str] :

    with open(data_file_name) as f:
        data = json.load(f)
    
    if department == "STPI":
        depart_category = "STPI"
    else :
        depart_category = "DEPARTMENT"

    tags = set()

    for item in get_tags_from_dict(data, "ITI", "3", "TP", "1", "1")[1]:

        tags.add(item)
    print(tags)


    


    return []


if __name__ == "__main__" :
    get_query_tags("../../data/department.json", "ITI", 3, [""], "")
