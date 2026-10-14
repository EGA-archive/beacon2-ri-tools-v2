"""Streaming writers for BFF output files.

The previous implementation reopened the output file, seeked to EOF and scanned
backwards for the closing bracket on every single record, which made writing BFF
files far slower than inserting the same records into MongoDB.  These writers
keep one buffered handle open for the whole run instead.
"""

import json
import os


class BffArrayWriter:
    """Streams documents into a single JSON array through one buffered handle.

    Produces the same document structure as before (one file holding a JSON
    array), so consumers such as ``mongoimport --jsonArray`` need no change.
    """

    def __init__(self, path):
        self.path = path
        self._handle = open(path, 'w')
        self._count = 0

    def write(self, doc):
        self._handle.write('[' if self._count == 0 else ',')
        json.dump(doc, self._handle)
        self._count += 1

    def write_many(self, docs):
        for doc in docs:
            self.write(doc)

    def close(self):
        if self._handle is None:
            return
        self._handle.write('[]' if self._count == 0 else ']')
        self._handle.close()
        self._handle = None


class BffLinesWriter:
    """Streams documents as JSON Lines, one compact document per line."""

    def __init__(self, path):
        self.path = path
        self._handle = open(path, 'w')
        self._count = 0

    def write(self, doc):
        json.dump(doc, self._handle)
        self._handle.write('\n')
        self._count += 1

    def write_many(self, docs):
        for doc in docs:
            self.write(doc)

    def close(self):
        if self._handle is None:
            return
        self._handle.close()
        self._handle = None


def open_bff_writer(directory, basename, jsonl=False):
    """Open a writer for ``<directory>/<basename>.json`` (or ``.jsonl``).

    The output directory is created if it does not exist yet.
    """
    os.makedirs(directory, exist_ok=True)
    if jsonl:
        return BffLinesWriter(os.path.join(directory, basename + '.jsonl'))
    return BffArrayWriter(os.path.join(directory, basename + '.json'))
