from dateutil.parser import parse
from pydantic import (
    BaseModel,
    PrivateAttr,
    field_validator
)
from typing import Optional

class Analyses(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    aligner: Optional[str] = None
    analysisDate: str
    biosampleId: Optional[str] = None
    id: str
    individualId: Optional[str] = None
    info: Optional[dict] = None
    pipelineName: str
    pipelineRef: Optional[str]=None
    runId: Optional[str]=None
    variantCaller: Optional[str]=None

    @field_validator('analysisDate')
    @classmethod
    def validate_analysis_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            parse(v)
        except Exception as e:
            raise ValueError(f'analysisDate must be a valid timestamp, error: {e}')
        return v
