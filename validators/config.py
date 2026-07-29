from typing import Any

from pydantic import BaseModel, model_validator

import biosamples

import csv


def csv_to_bff():
    filename = "biosamples3.csv"

    with open(filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)


    with open(filename, 'r' ) as theFile:
        reader = csv.DictReader(theFile)
        i=1
        for line in reader:
            dict_of_properties={}
            list_of_filled_items=[]
            for kline, vline in line.items():
                property_value = kline
                if property_value == None:
                    continue
                property_value=property_value.replace('\ufeff', '')


                
                valor = vline


                if i > 0:
                    
                    if valor != '':


                        list_of_filled_items.append(property_value)

                    if valor:
                        if '|' in valor:
                            dict_of_properties[property_value]=valor
                        else:
                            dict_of_properties[property_value]=valor
                        

                    elif valor == 0:
                        dict_of_properties[property_value]=valor

            #print(dict_properties)
            #print(dict_of_properties)

    return dict_of_properties

CONFIG = csv_to_bff()

print(CONFIG)

class ConfigModel(BaseModel):

    @model_validator(mode="before")
    @classmethod
    def populate_from_config(cls, data: Any):
        if data is None:
            data = {}
        elif not isinstance(data, dict):
            data = dict(data)

        merged = cls._config_to_dict()
        print('ready')
        print(data)
        cls._deep_update(merged, data)

        return merged

    @classmethod
    def _config_to_dict(cls):
        result = {}
        for key, value in CONFIG.items():
            parts = key.split("|")
            property_type=cls.__annotations__.get(parts[0])
            if 'list' in property_type:
                if parts[0] not in result:
                    result[parts[0]]=[]
            elif 'dict' in property_type:
                if parts[0] not in result:
                    result[parts[0]]={}
            elif property_type in ['str', 'int', 'float']:
                if parts[0] not in result:
                    result[parts[0]]=value
            else:
                if parts[0] not in result:
                    result[parts[0]]={}
            i=1
            while i < len(parts):
                print(key)
                print(value)
                property_type=cls.__annotations__.get(parts[i])
                if property_type == None:
                    print('whooo')
                    previous_type=cls.__annotations__.get(parts[i-1])
                    if previous_type != None:
                        if 'list' in previous_type:
                            print('heaaa')
                            formatted_type=previous_type.replace(']','[')
                            formatted_type = formatted_type.split('[')
                            formatted_type =formatted_type[1]
                            new_class = getattr(biosamples, formatted_type, None)
                            property_type=new_class.__annotations__.get(parts[i])
                            if result[parts[0]]==[]:
                                print(len(parts))
                                print(i)
                                if i+1==len(parts):
                                    result[parts[0]].append({parts[1]: value})
                                elif i+3==len(parts):
                                    result[parts[0]].append({parts[1]: {parts[2]: {parts[3]:value}}})
                                else:
                                    result[parts[0]].append({parts[1]: {parts[2]: value}})
                            else:
                                if i+1==len(parts):
                                    result[parts[0]][0][parts[1]]=value
                                else:
                                    print('hereeee')
                                    if parts[1] in result[parts[0]][0]:
                                        if i+1==len(parts):
                                            result[parts[0]][0][parts[1]][parts[2]]=value
                                        elif i+2==len(parts):
                                            result[parts[0]][0][parts[1]][parts[2]]=value
                                        else:
                                            if parts[2] not in result[parts[0]][0][parts[1]]:
                                                result[parts[0]][0][parts[1]][parts[2]]={}
                                                result[parts[0]][0][parts[1]][parts[2]][parts[3]]=value
                                            else:
                                                result[parts[0]][0][parts[1]][parts[2]][parts[3]]=value
                                                
                                    else:
                                        if i+1==len(parts):
                                            result[parts[0]][0][parts[1]]={}
                                            result[parts[0]][0][parts[1]][parts[2]]=value
                                        elif i+2==len(parts):
                                            if parts[1] not in result[parts[0]][0]:
                                                result[parts[0]][0][parts[1]]={}
                                                result[parts[0]][0][parts[1]][parts[2]]=value
                                        else:
                                            result[parts[0]][0][parts[1]]={}
                                            result[parts[0]][0][parts[1]][parts[2]]={}
                                            result[parts[0]][0][parts[1]][parts[2]][parts[3]]=value
                        else:
                            result[parts[0]][parts[1]]=value
                elif 'str' in property_type or 'int' in property_type or 'float' in property_type:
                    print('noteeeeeeeeed')
                    previous_type=cls.__annotations__.get(parts[i-1])
                    if previous_type == None:
                        previous_type=cls.__annotations__.get(parts[i-2])
                        if previous_type != None:
                            if 'list' in previous_type:
                                formatted_type=previous_type.replace(']','[')
                                formatted_type = formatted_type.split('[')
                                formatted_type =formatted_type[1]
                                new_class = getattr(biosamples, formatted_type, None)
                                property_type=new_class.__annotations__.get(parts[i-1])
                                if result[parts[0]]==[]:
                                    result[parts[0]].append({parts[1]: {parts[2]: value}})
                                else:
                                    print(parts)
                                    result[parts[0]][0][parts[1]]={}
                                    result[parts[0]][0][parts[1]][parts[2]]=value

                    else:
                        print(previous_type)
                        if 'list' in previous_type:
                            if result[parts[0]]==[]:
                                  result[parts[0]]=[{parts[i]: value}]
                            else:
                                result[parts[0]][0][parts[i]]=value
                        else:
                            result[parts[0]][parts[i]]=value


                i+=1
                print(result)
                
        return result

    @classmethod
    def _deep_update(cls, dst, src):
        for k, v in src.items():
            if (
                k in dst
                and isinstance(dst[k], dict)
                and isinstance(v, dict)
            ):
                cls._deep_update(dst[k], v)
            else:
                dst[k] = v