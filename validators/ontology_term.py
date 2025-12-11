import re
from pydantic import BaseModel, field_validator
from typing import Optional

class OntologyTerm(BaseModel, extra='forbid'):
    id: str
    label: Optional[str] = None

    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.fullmatch("[A-Za-z0-9]+:[A-Za-z0-9]+", v):
            return v

        raise ValueError('id must be CURIE, e.g. NCIT:C42331')
