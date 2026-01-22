import re
import argparse
from dateutil.parser import parse
from pydantic import (
    BaseModel,
    ValidationError,
    field_validator,
    Field,
    PrivateAttr
)

from typing import Optional, Union, List

from .common import OntologyTerm, timestamp_regex

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

class EventTimeline(BaseModel, extra='forbid'):
    end: Optional[str]=None
    start: Optional[str]=None
    @field_validator('end')
    @classmethod
    def check_end(cls, v: str) -> str:
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError('end, if string, must be Timestamp, getting this error: {}'.format(e))
            return v
    @field_validator('start')
    @classmethod
    def check_start(cls, v: str) -> str:
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError('start, if string, must be Timestamp, getting this error: {}'.format(e))
            return v
        

class Diseases(BaseModel, extra='forbid'):
    ageOfOnset: Optional[Union[str,dict]]=None
    diseaseCode: OntologyTerm
    familyHistory: Optional[bool]=None
    notes: Optional[str]=None
    severity: Optional[OntologyTerm]=None
    stage: Optional[OntologyTerm]=None
    @field_validator('ageOfOnset')
    @classmethod
    def check_ageOfOnset(cls, v: Optional[Union[str,dict]]) -> Optional[Union[str,dict]]:
        if v is None:
            return v
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
            except Exception as e:
                raise ValueError('ageOfOnset, if string, must be Timestamp, getting this error: {}'.format(e))
            return v
        elif isinstance(v, dict):
            for model in [Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm]:
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('ageOfOnset, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')
            
class Ethnicity(BaseModel, extra='forbid'):
    id: str
    label: Optional[str]=None
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. NCIT:C42331')
        return v
    
class Sex(BaseModel, extra='forbid'):
    id: str
    label: Optional[str]=None
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. NCIT:C42331')
        return v
    
class Reference(BaseModel, extra='forbid'):
    id: Optional[str] = None
    notes: Optional[str] = None
    reference: Optional[str] = None
    
class Evidence(BaseModel, extra='forbid'):
    evidenceCode: OntologyTerm
    reference: Optional[Reference] = None

class PhenotypicFeatures(BaseModel, extra='forbid'):
    evidence: Optional[Evidence]=None
    id: Optional[str] = None
    excluded: Optional[bool]=None
    featureType: OntologyTerm
    modifiers: Optional[List[OntologyTerm]]=None
    notes: Optional[str]=None
    onset: Optional[Union[str,dict]]=None
    resolution: Optional[Union[str,dict]]=None
    severity: Optional[OntologyTerm]=None
    @field_validator('modifiers')
    @classmethod
    def check_modifiers(cls, v: list) -> list:
        for modifier in v:
            OntologyTerm(**modifier)
    @field_validator('onset')
    @classmethod
    def check_onset(cls, v: Optional[Union[str,dict]]) -> Optional[Union[str,dict]]:
        if v is None:
            return v
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
                return v
            except Exception as e:
                raise ValueError('onset, if string, must be Timestamp, getting this error: {}'.format(e))
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
    def check_resolution(cls, v: Optional[Union[str,dict]]) -> Optional[Union[str,dict]]:
        if v is None:
            return v
        if isinstance(v, str):
            try:
                timestamp_regex.match(v)
                return v
            except Exception as e:
                raise ValueError('resolution, if string, must be Timestamp, getting this error: {}'.format(e))
        elif isinstance(v, dict):
            for model in [Age, AgeRange, GestationalAge, TimeInterval, OntologyTerm]:
                try:
                    model(**v)
                    return v
                except Exception:
                    continue
            raise ValueError('resolution, if object, must be any format possible between age, ageRange, gestationalAge, timeInterval or OntologyTerm')

class CohortCriteria(BaseModel, extra='forbid'):
    ageRange: Optional[AgeRange]=None
    diseaseConditions: Optional[List[Diseases]]=None
    ethnicities: Optional[List[OntologyTerm]]=None
    genders: Optional[List[OntologyTerm]]=None
    locations: Optional[List[OntologyTerm]]=None
    phenotypicConditions: Optional[List[PhenotypicFeatures]]=None

class DataAvailabilityAndDistribution(BaseModel, extra='forbid'):
    availability: bool
    availabilityCount: Optional[int]=None
    distribution: Optional[dict]=None
            
class CollectionEvent(BaseModel, extra='forbid'):
    eventAgeRange: Optional[DataAvailabilityAndDistribution]=None
    eventCases: Optional[int] = None
    eventControls: Optional[int] = None
    eventDataTypes: Optional[DataAvailabilityAndDistribution]=None
    eventDate: Optional[str]=None
    eventDiseases: Optional[DataAvailabilityAndDistribution]=None
    eventEthnicities: Optional[DataAvailabilityAndDistribution]=None
    eventGenders: Optional[DataAvailabilityAndDistribution]=None
    eventLocations: Optional[DataAvailabilityAndDistribution]=None
    eventNum: Optional[int] = None
    eventPhenotypes: Optional[DataAvailabilityAndDistribution]=None
    eventSize: Optional[int] = None
    eventTimeline: Optional[EventTimeline] = None
    @field_validator('eventDate')
    @classmethod
    def check_eventDate(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            timestamp_regex.match(v)
        except Exception as e:
            raise ValueError('eventDate, if string, must be Timestamp, getting this error: {}'.format(e))
        return v

class Cohorts(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    cohortDataTypes: Optional[List[OntologyTerm]] = None
    cohortDesign: Optional[OntologyTerm] = None
    cohortSize: Optional[int] = None
    cohortType: str
    collectionEvents: Optional[List[CollectionEvent]] = None
    exclusionCriteria: Optional[CohortCriteria] = None
    id: str
    inclusionCriteria: Optional[CohortCriteria] = None
    name: str
