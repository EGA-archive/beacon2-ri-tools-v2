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

class EventTimeline(BaseModel, extra='allow'):
    end: str | None=None
    start: str | None=None
    @field_validator('end')
    @classmethod
    def check_end(cls, v: str) -> str:
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'end, if string, must be Timestamp, getting this error: {e}')
            return v
    @field_validator('start')
    @classmethod
    def check_start(cls, v: str) -> str:
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'start, if string, must be Timestamp, getting this error: {e}')
            return v


class Diseases(BaseModel, extra='allow'):
    ageOfOnset: str | dict | None=None
    diseaseCode: OntologyTerm
    familyHistory: bool | None=None
    notes: str | None=None
    severity: OntologyTerm | None=None
    stage: OntologyTerm | None=None
    @field_validator('ageOfOnset')
    @classmethod
    def check_ageOfOnset(cls, v: str | dict | None) -> str | dict | None:
        if v is None:
            return v
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError(f'ageOfOnset, if string, must be Timestamp, getting this error: {e}')
            return v
        elif isinstance(v, dict):
            for model in [Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm]:
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

class Reference(BaseModel, extra='allow'):
    id: str | None = None
    notes: str | None = None
    reference: str | None = None

class Evidence(BaseModel, extra='allow'):
    evidenceCode: OntologyTerm
    reference: Reference | None = None

class PhenotypicFeatures(BaseModel, extra='allow'):
    evidence: Evidence | None=None
    id: str | None = None
    excluded: bool | None=None
    featureType: OntologyTerm
    modifiers: list[OntologyTerm] | None=None
    notes: str | None=None
    onset: str | dict | None=None
    resolution: str | dict | None=None
    severity: OntologyTerm | None=None
    @field_validator('modifiers')
    @classmethod
    def check_modifiers(cls, v: list) -> list:
        for modifier in v:
            OntologyTerm(**modifier)
    @field_validator('onset')
    @classmethod
    def check_onset(cls, v: str | dict | None) -> str | dict | None:
        if v is None:
            return v
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
                return v
            except Exception as e:
                raise ValueError(f'onset, if string, must be Timestamp, getting this error: {e}')
        elif isinstance(v, dict):
            for model in [Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm]:
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('onset, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')
    @field_validator('resolution')
    @classmethod
    def check_resolution(cls, v: str | dict | None) -> str | dict | None:
        if v is None:
            return v
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
                return v
            except Exception as e:
                raise ValueError(f'resolution, if string, must be Timestamp, getting this error: {e}')
        elif isinstance(v, dict):
            for model in [Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm]:
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('resolution, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class CohortCriteria(BaseModel, extra='allow'):
    ageRange: AgeRange | None=None
    diseaseConditions: list[Diseases] | None=None
    ethnicities: list[OntologyTerm] | None=None
    genders: list[OntologyTerm] | None=None
    locations: list[OntologyTerm] | None=None
    phenotypicConditions: list[PhenotypicFeatures] | None=None

class DataAvailabilityAndDistribution(BaseModel, extra='allow'):
    availability: bool
    availabilityCount: int | None=None
    distribution: dict | None=None

class CollectionEvent(BaseModel, extra='allow'):
    eventAgeRange: DataAvailabilityAndDistribution | None=None
    eventCases: int | None = None
    eventControls: int | None = None
    eventDataTypes: DataAvailabilityAndDistribution | None=None
    eventDate: str | None=None
    eventDiseases: DataAvailabilityAndDistribution | None=None
    eventEthnicities: DataAvailabilityAndDistribution | None=None
    eventGenders: DataAvailabilityAndDistribution | None=None
    eventLocations: DataAvailabilityAndDistribution | None=None
    eventNum: int | None = None
    eventPhenotypes: DataAvailabilityAndDistribution | None=None
    eventSize: int | None = None
    eventTimeline: EventTimeline | None = None
    @field_validator('eventDate')
    @classmethod
    def check_eventDate(cls, v: str | None) -> str | None:
        if v is None:
            return v
        try:
            timestamp_regex.match(v)
        except Exception as e:
            raise ValueError(f'eventDate, if string, must be Timestamp, getting this error: {e}')
        return v

class Cohorts(BaseModel, extra='allow'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: str | None = PrivateAttr()
    cohortDataTypes: list[OntologyTerm] | None = None
    cohortDesign: OntologyTerm | None = None
    cohortSize: int | None = None
    cohortType: str
    collectionEvents: list[CollectionEvent] | None = None
    exclusionCriteria: CohortCriteria | None = None
    id: str
    inclusionCriteria: CohortCriteria | None = None
    name: str
