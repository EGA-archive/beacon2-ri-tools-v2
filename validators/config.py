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
    def _get_properties(cls, type_class, parts, pos):
        print(type_class)
        if type_class not in ['str', 'int', 'float']:
            if 'list' in type_class:
                formatted_type=type_class.replace(']','[')
                formatted_type = formatted_type.split('[')
                formatted_type =formatted_type[1]
                module_name = cls.ENTRY_TYPE

                individuals = importlib.import_module(f"validators.{cls.MODEL}.{module_name}")

                new_class = getattr(individuals, formatted_type, None)
                property_type=new_class.__annotations__.get(parts[pos])
            elif '|' in type_class:
                formatted_type = type_class.split('|')

                
                
                
                module_name = cls.ENTRY_TYPE
                individuals = importlib.import_module(f"validators.{cls.MODEL}.{module_name}")
                for possible_type in formatted_type:
                    replaced_type = possible_type.replace(' ', '')
                    print(replaced_type)
                    new_class = getattr(individuals, replaced_type, None)
                    if new_class == None:
                        return 'None', False
                    property_type=new_class.__annotations__.get(parts[pos])
                    if property_type != None:
                        if 'list' in property_type:
                            return property_type, "list" in property_type
            else:
                property_type = 'None'
        else:
            property_type = type_class
        if property_type == None:
            property_type = 'None'
        return property_type, "list" in property_type

    @classmethod
    def _insert(cls, root, parts, list_flags, value):
        node = root

        for i, key in enumerate(parts[:-1]):

            is_list = list_flags[i]

            # If we are currently inside a list, descend into its first element.
            if isinstance(node, list):
                if not node:
                    node.append({})
                elif not isinstance(node[0], dict):
                    node[0] = {}
                node = node[0]

            # Create (or repair) the container for this key.
            if is_list:
                if key not in node or not isinstance(node[key], list):
                    node[key] = [{}]
            else:
                if key not in node or not isinstance(node[key], dict):
                    node[key] = {}

            node = node[key]

        # If the parent of the leaf is a list, descend into its first element.
        if isinstance(node, list):
            if not node:
                node.append({})
            elif not isinstance(node[0], dict):
                node[0] = {}
            node = node[0]

        # Handle the leaf field.
        if list_flags[-1]:
            if parts[-1] not in node or not isinstance(node[parts[-1]], list):
                node[parts[-1]] = []
            node[parts[-1]].append(value)
        else:
            node[parts[-1]] = value

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
            if 'DataTypesArray' in property_type:
                try:
                    result[parts[0]][0][parts[1]]= value
                except Exception:
                    result[parts[0]]= [{parts[1]:value}]


                continue
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
            print(parts)
            while i < len(parts):

                # only handle the leaf assignment
                if i + 1 == len(parts):

                    types = []
                    flags = []

                    current = cls.__annotations__.get(parts[0])

                    if current is None:
                        break

                    types.append(current)
                    flags.append("list" in current)

                    for pos in range(1, len(parts)):
                        current, is_list = cls._get_properties(
                            current,
                            parts,
                            pos
                        )

                        types.append(current)
                        flags.append(is_list)
                    if 'aminoacidChange' in parts:
                        print(types)
                        print(parts)
                        print(value)
                        print(flags)
                    cls._insert(
                        result,
                        parts,
                        flags,
                        value
                    )
                    print(result)


                i+=1
        print(result)
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