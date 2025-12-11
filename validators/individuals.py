from dateutil.parser import parse
from pydantic import (
    BaseModel,
    field_validator,
    Field,
    PrivateAttr
)

from typing import Optional, Union
from .ontology_term import OntologyTerm

class Age(BaseModel, extra='forbid'):
    iso8601duration: str

class AgeRange(BaseModel, extra='forbid'):
    end: Age
    start: Age

class GestationalAge(BaseModel, extra='forbid'):
    days: Optional[int] = None
    weeks: int

class TimeInterval(BaseModel, extra='forbid'):
    end: str
    start: str

class ReferenceRange(BaseModel, extra='forbid'):
    high: Union[int,float]
    low: Union[int, float]
    unit: OntologyTerm

class Quantity(BaseModel, extra='forbid'):
    referenceRange: Optional[ReferenceRange] = None
    unit: OntologyTerm
    value: Union[int, float]

class TypedQuantity(BaseModel, extra='forbid'):
    quantity: Quantity
    quantityType: OntologyTerm

class TypedQuantities(BaseModel):
    typedQuantities: TypedQuantity

class Members(BaseModel, extra='forbid'):
    affected: bool
    memberId: str
    role: OntologyTerm

class Reference(BaseModel, extra='forbid'):
    id: Optional[str] = None
    notes: Optional[str] = None
    reference: Optional[str] = None

class Evidence(BaseModel, extra='forbid'):
    evidenceCode: OntologyTerm
    reference: Optional[Reference] = None

class DoseIntervals(BaseModel, extra='forbid'):
    interval: Union[str,dict]
    quantity: Quantity
    scheduleFrequency: OntologyTerm

    @field_validator('interval')
    @classmethod
    def check_interval(cls, v: Union[str,dict]) -> Union[str,dict]:
        if isinstance(v, str):
            try:
                parse(v)
            except Exception as e:
                raise ValueError('interval, if string, must be Timestamp, getting this error: {}'.format(e))
            return v
        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('interval, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Diseases(BaseModel, extra='forbid'):
    ageOfOnset: Optional[Union[str,dict]]=None
    diseaseCode: OntologyTerm
    familyHistory: Optional[bool]=None
    notes: Optional[str]=None
    severity: Optional[OntologyTerm]=None
    stage: Optional[OntologyTerm]=None
    @field_validator('ageOfOnset')
    @classmethod
    def check_ageOfOnset(cls, v: Union[str,dict]) -> Union[str,dict]:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                parse(v)
            except Exception as e:
                raise ValueError('ageOfOnset, if string, must be Timestamp, getting this error: {}'.format(e))
            return v
        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('ageOfOnset, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Exposures(BaseModel, extra='forbid'):
    ageAtExposure: Age
    date: Optional[str] = None
    duration: str
    exposureCode: OntologyTerm
    unit: OntologyTerm
    value: Optional[Union[int, float]] = None

class InterventionsOrProcedures(BaseModel, extra='forbid'):
    ageAtProcedure: Optional[Union[str,dict]]=None
    bodySite: Optional[OntologyTerm]=None
    dateOfProcedure: Optional[str]=None
    procedureCode: OntologyTerm
    @field_validator('ageAtProcedure')
    @classmethod
    def check_ageAtProcedure(cls, v: Union[str,dict]) -> Union[str,dict]:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                parse(v)
            except Exception as e:
                raise ValueError('ageAtProcedure, if string, must be Timestamp, getting this error: {}'.format(e))
            return v
        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('ageAtProcedure, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Measurement(BaseModel, extra='forbid'):
    assayCode: OntologyTerm
    date: Optional[str] = None
    measurementValue: Union[Quantity, OntologyTerm, TypedQuantities]
    notes: Optional[str]=None
    observationMoment: Optional[Union[str,dict]]=None
    procedure: Optional[InterventionsOrProcedures] = None
    @field_validator('observationMoment')
    @classmethod
    def check_observationMoment(cls, v: Union[str,dict]) -> Union[str,dict]:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                parse(v)
            except Exception as e:
                raise ValueError('observationMoment, if string, must be Timestamp, getting this error: {}'.format(e))
            return v

        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('observationMoment, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Pedigrees(BaseModel, extra='forbid'):
    disease: Diseases
    id: str
    members: list[Members]
    numSubjects: Optional[int] = None

class PhenotypicFeatures(BaseModel, extra='forbid'):
    evidence: Optional[Evidence]=None
    id: Optional[str] = None
    excluded: Optional[bool]=None
    featureType: OntologyTerm
    modifiers: Optional[list[OntologyTerm]]=None
    notes: Optional[str]=None
    onset: Optional[Union[str,dict]]=None
    resolution: Optional[Union[str,dict]]=None
    severity: Optional[OntologyTerm]=None
    @field_validator('onset')
    @classmethod
    def check_onset(cls, v: Union[str,dict]) -> Union[str,dict]:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                parse(v)
            except Exception as e:
                raise ValueError('onset, if string, must be Timestamp, getting this error: {}'.format(e))
            return v

        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue

            raise ValueError('onset, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

    @field_validator('resolution')
    @classmethod
    def check_resolution(cls, v: Union[str,dict]) -> Union[str,dict]:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                parse(v)
            except Exception as e:
                raise ValueError('resolution, if string, must be Timestamp, getting this error: {}'.format(e))
            return v

        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('resolution, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Treatment(BaseModel, extra='forbid'):
    ageAtOnset: Optional[Age] = None
    cumulativeDose: Optional[Quantity] = None
    doseIntervals: Optional[list[DoseIntervals]] = None
    routeOfAdministration: Optional[OntologyTerm] = None
    treatmentCode: OntologyTerm

class Individuals(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    diseases: Optional[list[Diseases]] = None
    ethnicity: Optional[OntologyTerm] = None
    exposures: Optional[list[Exposures]] = None
    geographicOrigin: Optional[OntologyTerm] = None
    id: str
    info: Optional[dict] = None
    interventionsOrProcedures: Optional[list[InterventionsOrProcedures]] = None
    karyotypicSex: Optional[str] = None
    measures: Optional[list[Measurement]]=None
    pedigrees: Optional[list[Pedigrees]] = None
    phenotypicFeatures: Optional[list[PhenotypicFeatures]] = None
    sex: OntologyTerm
    treatments: Optional[list[Treatment]] = None

    @field_validator('karyotypicSex')
    @classmethod
    def check_karyotypic(cls, v: str) -> str:
        karyotypic_values=[
                "UNKNOWN_KARYOTYPE",
                "XX",
                "XY",
                "XO",
                "XXY",
                "XXX",
                "XXYY",
                "XXXY",
                "XXXX",
                "XYY",
                "OTHER_KARYOTYPE"]
        if v not in karyotypic_values:
            raise ValueError('id must be one from {}'.format(karyotypic_values))
        return v
