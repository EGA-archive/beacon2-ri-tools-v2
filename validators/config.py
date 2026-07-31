from pydantic import BaseModel, model_validator, RootModel
import ast
from typing import Any, Union
from copy import deepcopy
from typing import get_origin, get_args, get_type_hints
import importlib
from types import UnionType

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
        if type_class is None:
            return "None", False

        type_class = type_class.strip()

        if "|" in type_class:
            candidates = [
                t.strip()
                for t in type_class.split("|")
                if t.strip() != "None"
            ]

            if len(candidates) == 1:
                type_class = candidates[0]


        if type_class in ["str", "int", "float", "bool"]:
            return type_class, False

        module_name = cls.ENTRY_TYPE
        individuals = importlib.import_module(
            f"validators.{cls.MODEL}.{module_name}"
        )

        # List type: list[Something]
        if type_class.startswith("list["):
            inner_type = type_class[len("list["):-1]

            new_class = getattr(individuals, inner_type, None)

            if new_class is None:
                return "None", False

            property_type = new_class.__annotations__.get(parts[pos])

            if property_type is None:
                return "None", False

            return property_type, "list" in property_type


        if "|" in type_class:
            possible_types = [
                t.strip()
                for t in type_class.split("|")
                if t.strip() != "None"
            ]

            for possible_type in possible_types:
                new_class = getattr(individuals, possible_type, None)

                if new_class is None:
                    continue

                property_type = new_class.__annotations__.get(parts[pos])

                if property_type is not None:
                    return property_type, "list" in property_type

            return "None", False


        # Normal model/class
        new_class = getattr(individuals, type_class, None)

        if new_class is None:
            return "None", False

        property_type = new_class.__annotations__.get(parts[pos])

        if property_type is None:
            return "None", False

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

        if isinstance(node, list):
            if not node:
                node.append({})
            elif not isinstance(node[0], dict):
                node[0] = {}
            node = node[0]

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
            tp = get_type_hints(cls)[parts[0]]
            if get_origin(tp) is UnionType:
                tp = next(t for t in get_args(tp) if t is not type(None))
            try:
                if issubclass(tp, RootModel):
                    tp = tp.__annotations__["root"]

                if 'list' in tp:
                    pass

            except Exception:
                tp='None'

            if key == 'info':
                result['info']={"info": value}
            elif 'list' in property_type:
                if parts[0] not in result:
                    if len(parts)==1:
                        result[parts[0]]=[value]
                    else:
                        result[parts[0]]=[]
            elif 'list' in tp:
                try:
                    result[parts[0]][0][parts[1]]= value
                except Exception:
                    result[parts[0]]= [{parts[1]:value}]
                continue
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

                    cls._insert(
                        result,
                        parts,
                        flags,
                        value
                    )



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