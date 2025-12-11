from dateutil.parser import parse
from pydantic import (
    BaseModel,
    field_validator,
    PrivateAttr
)

from typing import Optional, List
from .ontology_term import OntologyTerm

class DUODataUse(OntologyTerm, extra='forbid'):
    modifiers: Optional[List[OntologyTerm]] = None
    version: str

class DataUseConditions(BaseModel, extra='forbid'):
    duoDataUse: Optional[List[DUODataUse]] = None

class Datasets(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    createDateTime: Optional[str] = None
    dataUseConditions: Optional[DataUseConditions]=None
    description: Optional[str] = None
    externalUrl: Optional[str] = None
    id: str
    info: Optional[dict] = None
    name: str
    updateDateTime: Optional[str]=None
    version: Optional[str] = None

    @field_validator('createDateTime')
    @classmethod
    def check_createDateTime(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v

        try:
            parse(v)
        except Exception as e:
            raise ValueError('createDateTime, if string, must be Timestamp, getting this error: {}'.format(e))
        return v

    @field_validator('updateDateTime')
    @classmethod
    def check_updateDateTime(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v

        try:
            parse(v)
        except Exception as e:
            raise ValueError('updateDateTime, if string, must be Timestamp, getting this error: {}'.format(e))
        return v
