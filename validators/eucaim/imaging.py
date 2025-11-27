import re
from dateutil.parser import parse

from pydantic import (
    BaseModel,
    field_validator,
    PrivateAttr
)
from typing import Optional

class OntologyTerm(BaseModel):
    id: str
    label: Optional[str]=None
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. EUCAIM:COM1001288')
        return v.title()

class Imaging(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    imagingId: str
    patientId: str
    diseaseId: Optional[str]=None
    imageModality: OntologyTerm
    imageBodypart: OntologyTerm
    imageManufacturer: OntologyTerm
    dateOfImageAcquisition: str
    @field_validator('dateOfImageAcquisition')
    @classmethod
    def check_dateOfImageAcquisition(cls, v: str) -> str:
        if isinstance(v, str):
            try:
                parse(v)
            except Exception as e:
                raise ValueError('dateOfImageAcquisition, if string, must be a date, getting this error: {}'.format(e))
            return v