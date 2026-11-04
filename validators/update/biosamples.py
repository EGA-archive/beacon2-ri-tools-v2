from pydantic import BaseModel, PrivateAttr, field_validator

from .common import OntologyTerm, timestamp_regex


class Age(BaseModel, extra='allow'):
    iso8601duration: str

class AgeRange(BaseModel, extra='allow'):
    end: Age
    start: Age

class GestationalAge(BaseModel, extra='allow'):
    days: int | None = None
    weeks: int

class TimeInterval(BaseModel, extra='allow'):
    end: str
    start: str

class ReferenceRange(BaseModel, extra='allow'):
    high: int | float
    low: int | float
    unit: OntologyTerm

class Quantity(BaseModel, extra='allow'):
    referenceRange: ReferenceRange | None = None
    unit: OntologyTerm
    value: int | float

class TypedQuantity(BaseModel, extra='allow'):
    quantity: Quantity
    quantityType: OntologyTerm

class TypedQuantities(BaseModel):
    typedQuantities: TypedQuantity

class InterventionsOrProcedures(BaseModel, extra='allow'):
    ageAtProcedure: str | dict | None=None
    bodySite: OntologyTerm | None=None
    dateOfProcedure: str | None=None
    procedureCode: OntologyTerm
    @field_validator('ageAtProcedure')
    @classmethod
    def check_ageAtProcedure(cls, v: str | dict | None) -> str | dict | None:
        if v is None:
            return v
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
                return v
            except Exception as e:
                raise ValueError(f'ageAtProcedure, if string, must be Timestamp, getting this error: {e}')
        elif isinstance(v, dict):
            for model in [Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm]:
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('ageAtProcedure, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Measurement(BaseModel, extra='allow'):
    assayCode: OntologyTerm
    date: str | None = None
    measurementValue: Quantity | OntologyTerm | TypedQuantities
    notes: str | None=None
    observationMoment: str | dict | None=None
    procedure: InterventionsOrProcedures | None = None
    @field_validator('observationMoment')
    @classmethod
    def check_observationMoment(cls, v: str | dict | None) -> str | dict | None:
        if v is None:
            return v
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
                return v
            except Exception as e:
                raise ValueError(f'observationMoment, if string, must be Timestamp, getting this error: {e}')
        elif isinstance(v, dict):
            for model in [Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm]:
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('observationMoment, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Biosamples(BaseModel, extra='allow'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: str | None = PrivateAttr()
    biosampleStatus: OntologyTerm
    collectionDate: str | None = None
    collectionMoment: str | None = None
    diagnosticMarkers: list[OntologyTerm] | None = None
    histologicalDiagnosis: OntologyTerm | None = None
    id: str
    individualId: str | None = None
    info: dict | None = None
    measurements: list[Measurement] | None = None
    notes: str | None=None
    obtentionProcedure: InterventionsOrProcedures | None = None
    pathologicalStage: OntologyTerm | None = None
    pathologicalTnmFinding: list | None = None
    phenotypicFeatures: list | None = None
    sampleOriginDetail: OntologyTerm | None = None
    sampleOriginType: OntologyTerm
    sampleProcessing: OntologyTerm | None = None
    sampleStorage: OntologyTerm | None = None
    tumorGrade: OntologyTerm | None = None
    tumorProgression: OntologyTerm | None = None
