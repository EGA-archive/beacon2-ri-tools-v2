#!/usr/bin/env python3

import csv
import json
import sys
from urllib.parse import urldefrag, urljoin

import requests


class SchemaLoader:
    def __init__(self):
        self.cache = {}

    def load(self, uri):
        if uri in self.cache:
            return self.cache[uri]

        if uri.startswith(("http://", "https://")):
            response = requests.get(uri, timeout=60)
            response.raise_for_status()
            schema = response.json()
        else:
            raise ValueError(
                f"Only URLs are supported. Received: {uri}"
            )

        self.cache[uri] = schema
        return schema


loader = SchemaLoader()


def resolve_json_pointer(document, pointer):
    """
    Resolve JSON pointer fragments like:
    /$defs/Address
    /definitions/Address
    """

    if not pointer:
        return document

    if pointer.startswith("/"):
        pointer = pointer[1:]

    current = document

    for part in pointer.split("/"):
        part = part.replace("~1", "/")
        part = part.replace("~0", "~")
        current = current[part]

    return current


def resolve_ref(ref, current_uri):
    """
    Resolve:
      #/$defs/X
      ./common.json
      ./common.json#/$defs/X
      https://example.com/schema.json
    """

    if ref.startswith("#"):
        document = loader.load(current_uri)
        return (
            resolve_json_pointer(document, ref[1:]),
            current_uri
        )

    target_uri, fragment = urldefrag(
        urljoin(current_uri, ref)
    )

    document = loader.load(target_uri)

    if fragment:
        document = resolve_json_pointer(
            document,
            fragment
        )

    return document, target_uri


def extract_paths(schema, uri, prefix, paths, visited):
    if not isinstance(schema, dict):
        return

    # Resolve references
    while "$ref" in schema:
        ref = schema["$ref"]

        key = (
            uri,
            ref,
            tuple(prefix)
        )

        if key in visited:
            return

        visited.add(key)

        schema, uri = resolve_ref(
            ref,
            uri
        )

    # Composition
    for keyword in ("allOf", "anyOf", "oneOf"):
        if keyword in schema:
            for subschema in schema[keyword]:
                extract_paths(
                    subschema,
                    uri,
                    prefix,
                    paths,
                    visited.copy()
                )
            return

    # Objects
    if "properties" in schema:
        for name, subschema in schema["properties"].items():
            extract_paths(
                subschema,
                uri,
                prefix + [name],
                paths,
                visited.copy()
            )
        return

    # Arrays
    if schema.get("type") == "array":
        items = schema.get("items")
        if items:
            extract_paths(
                items,
                uri,
                prefix,
                paths,
                visited.copy()
            )
        return

    # Leaf
    if prefix:
        paths.add("|".join(prefix))


def main():
    if len(sys.argv) != 4:
        print(
            "Usage:\n"
            "  python jsonschema_to_csv.py "
            "<schema_url> <output.csv> <output.txt>"
        )
        sys.exit(1)

    schema_url = sys.argv[1]
    output_csv = sys.argv[2]
    output_headers = sys.argv[3]

    root_schema = loader.load(schema_url)

    paths = set()

    extract_paths(
        root_schema,
        schema_url,
        [],
        paths,
        set()
    )

    with open(
        output_csv,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(sorted(paths))

    print(
        f"Generated {len(paths)} headers into {output_csv}"
    )

    with open(output_headers, "w") as f:
        for item in sorted(paths):
            f.write(f"{item}\n")

    print(
        f"Generated header file into {output_headers}"
    )

if __name__ == "__main__":
    main()