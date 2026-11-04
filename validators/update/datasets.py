import re

from pydantic import BaseModel, PrivateAttr, field_validator

from .common import OntologyTerm, timestamp_regex


class DUODataUse(BaseModel, extra='allow'):
    id: str
    label: str | None=None
    modifiers: list[OntologyTerm] | None = None
    version: str
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. NCIT:C42331')
        return v
    @field_validator('modifiers')
    @classmethod
    def check_modifiers(cls, v: list) -> list:
        for modifier in v:
            OntologyTerm(**modifier)

class DataUseConditions(BaseModel, extra='allow'):
    duoDataUse: list[DUODataUse] | None = None

class Datasets(BaseModel, extra='allow'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: str | None = PrivateAttr()
    createDateTime: str | None = None
    dataUseConditions: DataUseConditions | None=None
    description: str | None = None
    externalUrl: str | None = None
    id: str
    info: dict | None = None
    name: str
    updateDateTime: str | None=None
    version: str | None = None
    @field_validator('createDateTime')
    @classmethod
    def check_createDateTime(cls, v: str | None) -> str | None:
        if v is None:
            return v
        try:
            timestamp_regex.match(v)
        except Exception as e:
            raise ValueError(f'createDateTime, if string, must be Timestamp, getting this error: {e}')
        return v
    @field_validator('updateDateTime')
    @classmethod
    def check_updateDateTime(cls, v: str | None) -> str | None:
        if v is None:
            return v
        try:
            timestamp_regex.match(v)
        except Exception as e:
            raise ValueError(f'updateDateTime, if string, must be Timestamp, getting this error: {e}')
        return v
