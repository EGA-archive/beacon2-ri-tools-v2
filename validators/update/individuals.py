import re

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

class Members(BaseModel, extra='allow', strict=True):
    affected: bool
    memberId: str
    role: OntologyTerm

class Reference(BaseModel, extra='allow'):
    id: str | None = None
    notes: str | None = None
    reference: str | None = None

class Evidence(BaseModel, extra='allow'):
    evidenceCode: OntologyTerm
    reference: Reference | None = None

class DoseIntervals(BaseModel, extra='allow'):
    interval: str | dict
    quantity: Quantity
    scheduleFrequency: OntologyTerm
    @field_validator('interval')
    @classmethod
    def check_interval(cls, v: str | dict) -> str | dict:
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'interval, if string, must be Timestamp, getting this error: {e}')
            return v
        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('interval, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Diseases(BaseModel, extra='allow', strict=True):
    ageOfOnset: str | dict | None=None
    diseaseCode: OntologyTerm
    familyHistory: bool | None=None
    notes: str | None=None
    severity: OntologyTerm | None=None
    stage: OntologyTerm | None=None
    @field_validator('ageOfOnset')
    @classmethod
    def check_ageOfOnset(cls, v: str | dict) -> str | dict:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'ageOfOnset, if string, must be Timestamp, getting this error: {e}')
            return v
        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('ageOfOnset, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Ethnicity(BaseModel, extra='allow'):
    id: str
    label: str | None=None
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. NCIT:C42331')
        return v

class Exposures(BaseModel, extra='allow'):
    ageAtExposure: Age
    date: str | None = None
    duration: str
    exposureCode: OntologyTerm
    unit: OntologyTerm
    value: int | float | None = None

class GeographicOrigin(BaseModel, extra='allow'):
    id: str
    label: str | None=None
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. NCIT:C42331')
        return v

class InterventionsOrProcedures(BaseModel, extra='allow'):
    ageAtProcedure: str | dict | None=None
    bodySite: OntologyTerm | None=None
    dateOfProcedure: str | None=None
    procedureCode: OntologyTerm
    @field_validator('ageAtProcedure')
    @classmethod
    def check_ageAtProcedure(cls, v: str | dict) -> str | dict:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'ageAtProcedure, if string, must be Timestamp, getting this error: {e}')
            return v
        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
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
    def check_observationMoment(cls, v: str | dict) -> str | dict:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'observationMoment, if string, must be Timestamp, getting this error: {e}')
            return v

        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('observationMoment, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Pedigrees(BaseModel, extra='allow'):
    disease: Diseases
    id: str
    members: list[Members]
    numSubjects: int | None = None

class PhenotypicFeatures(BaseModel, extra='allow', strict=True):
    evidence: Evidence | None=None
    id: str | None = None
    excluded: bool | None=None
    featureType: OntologyTerm
    modifiers: list[OntologyTerm] | None=None
    notes: str | None=None
    onset: str | dict | None=None
    resolution: str | dict | None=None
    severity: OntologyTerm | None=None
    @field_validator('onset')
    @classmethod
    def check_onset(cls, v: str | dict) -> str | dict:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'onset, if string, must be Timestamp, getting this error: {e}')
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
    def check_resolution(cls, v: str | dict) -> str | dict:
        if v is None:
            return v

        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'resolution, if string, must be Timestamp, getting this error: {e}')
            return v

        elif isinstance(v, dict):
            for model in (Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm):
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('resolution, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class Sex(BaseModel, extra='allow'):
    id: str
    label: str | None=None
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. NCIT:C42331')
        return v

class Treatment(BaseModel, extra='allow'):
    ageAtOnset: Age | None = None
    cumulativeDose: Quantity | None = None
    doseIntervals: list[DoseIntervals] | None = None
    routeOfAdministration: OntologyTerm | None = None
    treatmentCode: OntologyTerm
    @field_validator('doseIntervals')
    @classmethod
    def check_doseIntervals(cls, v: list) -> list:
        for doseInterval in v:
            DoseIntervals(**doseInterval)

class Individuals(BaseModel, extra='allow'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: str | None = PrivateAttr()
    diseases: list[Diseases] | None = None
    ethnicity: OntologyTerm | None = None
    exposures: list[Exposures] | None = None
    geographicOrigin: OntologyTerm | None = None
    id: str
    info: dict | None = None
    interventionsOrProcedures: list[InterventionsOrProcedures] | None = None
    karyotypicSex: str | None = None
    measures: list[Measurement] | None=None
    pedigrees: list[Pedigrees] | None = None
    phenotypicFeatures: list[PhenotypicFeatures] | None = None
    sex: OntologyTerm
    treatments: list[Treatment] | None = None
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
            raise ValueError(f'id must be one from {karyotypic_values}')
        return v
