from pydantic import BaseModel, model_validator
import ast
from typing import Any, ClassVar
from copy import deepcopy
from typing import get_type_hints, get_origin, get_args
import importlib

def split_piped_object(obj):
    paths = []

    def collect(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                collect(v, path + [k])
        elif isinstance(node, list):
            return
        elif isinstance(node, str) and "|" in node:
            parts = node.split("|")
            paths.append((path, parts))

    collect(obj, [])

    if not paths:
        return None

    lengths = {len(parts) for _, parts in paths}
    if len(lengths) != 1:
        return None

    n = lengths.pop()

    result = []
    for i in range(n):
        new_obj = deepcopy(obj)
        for path, parts in paths:
            target = new_obj
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = parts[i]
        result.append(new_obj)

    return result


def expand(node):
    if isinstance(node, dict):
        return {k: expand(v) for k, v in node.items()}

    elif isinstance(node, list):
        new_list = []
        for item in node:
            item = expand(item)

            if isinstance(item, dict):
                expanded = split_piped_object(item)
                if expanded:
                    new_list.extend(expanded)
                else:
                    new_list.append(item)
            else:
                new_list.append(item)
        return new_list

    else:
        return node

class ConfigModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def populate_from_config(cls, data: Any, config_data):
        if data is None:
            data = {}
        elif not isinstance(data, dict):
            data = dict(data)

        merged = cls._config_to_dict()
        cls._deep_update(merged, data)

        return merged

    @classmethod
    def _config_to_dict(cls):

        result = {}
        for key, value in cls.CONFIG.items():
            try:
                value=ast.literal_eval(value)
            except Exception:
                pass
            parts = key.split("|")
            property_type=cls.__annotations__.get(parts[0])
            if key == 'info':
                result['info']={"info": value}
            elif 'list' in property_type:
                if parts[0] not in result:
                    if len(parts)==1:
                        result[parts[0]]=[value]
                    else:
                        result[parts[0]]=[]
            elif 'dict' in property_type:
                if parts[0] not in result:
                    if len(parts)==1:
                        result[parts[0]]=value
                    else:
                        result[parts[0]]={}
            elif property_type in ['str', 'int', 'float']:
                if parts[0] not in result:
                    result[parts[0]]=value
            else:
                if parts[0] not in result:
                    if len(parts)==1:
                        result[parts[0]]=value
                    else:
                        result[parts[0]]={}
            i=1
            while i < len(parts):
                property_type=cls.__annotations__.get(parts[i])
                if property_type == None:
                    previous_type=cls.__annotations__.get(parts[i-1])
                    if previous_type != None:
                        if 'list' in previous_type:
                            formatted_type=previous_type.replace(']','[')
                            formatted_type = formatted_type.split('[')
                            formatted_type =formatted_type[1]
                            module_name = cls.ENTRY_TYPE

                            individuals = importlib.import_module(f"validators.{cls.MODEL}.{module_name}")

                            new_class = getattr(individuals, formatted_type, None)

                            property_type=new_class.__annotations__.get(parts[i])
                            if result[parts[0]]==[]:
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
                                    if 'list' in property_type:
                                        try:
                                            result[parts[0]][0][parts[1]][0][parts[2]]=value
                                        except Exception as e:
                                            result[parts[0]][0][parts[1]]=[{parts[2]:value}]
                                    elif len(parts)==5:
                                        if parts[3] not in result[parts[0]][0][parts[1]][parts[2]]:
                                            result[parts[0]][0][parts[1]][parts[2]][parts[3]]={}
                                        if parts[4] not in result[parts[0]][0][parts[1]][parts[2]][parts[3]]:
                                            result[parts[0]][0][parts[1]][parts[2]][parts[3]][parts[4]]=value
                                        else:
                                            result[parts[0]][0][parts[1]][parts[2]][parts[3]][parts[4]]=value
                                    elif parts[1] in result[parts[0]][0]:
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
                            module_name = cls.ENTRY_TYPE
                            if 'LegacyVariation' in previous_type:
                                previous_type = 'LegacyVariation'
                            else:

                                previous_type = previous_type.split('|')
                                previous_type = previous_type[0].replace(" ", "")

                            individuals = importlib.import_module(f"validators.{cls.MODEL}.{module_name}")

                            new_class = getattr(individuals, previous_type, None)

                            property_type=new_class.__annotations__.get(parts[i])
                            if property_type != None:
                                if 'list' in property_type and i+1==len(parts):
                                    result[parts[0]][parts[1]]=[value]
                                elif len(parts)==2 and i+1==len(parts):
                                    result[parts[0]][parts[1]]=value
                                elif len(parts)==3 and 'list' not in property_type:
                                    result[parts[0]][parts[1]][parts[2]]=value
                                elif len(parts)==4 and i+1==len(parts):
                                    result[parts[0]][parts[1]][parts[2]][parts[3]]=value
                                elif len(parts)==5:
                                    try:
                                        result[parts[0]][parts[1]][parts[2]][parts[3]][parts[4]]=value
                                    except Exception:
                                        try:
                                            result[parts[0]][parts[1]][parts[2]][parts[3]]={}
                                            result[parts[0]][parts[1]][parts[2]][parts[3]][parts[4]]=value
                                        except Exception:
                                            try:
                                                result[parts[0]][parts[1]][parts[2]]={}
                                                result[parts[0]][parts[1]][parts[2]][parts[3]]={}
                                                result[parts[0]][parts[1]][parts[2]][parts[3]][parts[4]]=value
                                            except Exception:
                                                result[parts[0]][parts[1]]={}
                                                result[parts[0]][parts[1]][parts[2]]={}
                                                result[parts[0]][parts[1]][parts[2]][parts[3]]={}
                                                result[parts[0]][parts[1]][parts[2]][parts[3]][parts[4]]=value   
                            elif i+1==len(parts) and len(parts)==2:
                                result[parts[0]][parts[1]]=value


                    elif not isinstance(result[parts[0]],list):
                        if len(parts)==4 and i+1==len(parts):
                            try:
                                result[parts[0]][parts[1]][parts[2]][parts[3]]=value
                            except Exception:
                                try:
                                    result[parts[0]][parts[1]][parts[2]]={}
                                    result[parts[0]][parts[1]][parts[2]][parts[3]]=value

                                except Exception:
                                    result[parts[0]][parts[1]]={}
                                    result[parts[0]][parts[1]][parts[2]]={}
                                    result[parts[0]][parts[1]][parts[2]][parts[3]]=value

                elif 'str' in property_type or 'int' in property_type or 'float' in property_type:
                    previous_type=cls.__annotations__.get(parts[i-1])
                    if previous_type == None:
                        previous_type=cls.__annotations__.get(parts[i-2])
                        if previous_type != None:
                            if 'list' in previous_type:
                                formatted_type=previous_type.replace(']','[')
                                formatted_type = formatted_type.split('[')
                                formatted_type =formatted_type[1]
                                module_name = cls.ENTRY_TYPE

                                individuals = importlib.import_module(f"validators.{cls.MODEL}.{module_name}")

                                new_class = getattr(individuals, formatted_type, None)
                                property_type=new_class.__annotations__.get(parts[i-1])
                                if result[parts[0]]==[]:
                                    result[parts[0]].append({parts[1]: {parts[2]: value}})
                                else:
                                    try:
                                        result[parts[0]][0][parts[1]][0][parts[2]]=value
                                    except Exception:
                                        result[parts[0]][0][parts[1]]={}
                                        result[parts[0]][0][parts[1]][parts[2]]=value
                        else:
                            if len(parts)==5:
                                if parts[4] not in result[parts[0]][0][parts[1]][parts[2]][parts[3]]:
                                    result[parts[0]][0][parts[1]][parts[2]][parts[3]]={}
                                    result[parts[0]][0][parts[1]][parts[2]][parts[3]][parts[4]]=value
                                else:
                                    result[parts[0]][0][parts[1]][parts[2]][parts[3]][parts[4]]=value

                    else:
                        if 'list' in previous_type:
                            if result[parts[0]]==[]:
                                  result[parts[0]]=[{parts[i]: value}]
                            else:
                                result[parts[0]][0][parts[i]]=value
                        else:
                            result[parts[0]][parts[i]]=value

                i+=1
        definitivedict=expand(result)
                
        return definitivedict

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