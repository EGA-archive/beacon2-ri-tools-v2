from pydantic import BaseModel, PrivateAttr

from .common import OntologyTerm

#parser = argparse.ArgumentParser()
#parser.add_argument("-url", "--url")
#args = parser.parse_args()

class Runs(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: str | None = PrivateAttr()
    biosampleId: str
    id: str
    individualId: str | None = None
    info: dict | None = None
    libraryLayout: str | None=None
    librarySelection: str | None=None
    librarySource: OntologyTerm | None = None
    libraryStrategy: str | None = None
    platform: str | None = None
    platformModel: OntologyTerm | None = None
    runDate: str | None = None
    datasetId: str | None = None
