import json
import argparse
from pydantic import (
    BaseModel,
    ValidationError,
    PrivateAttr
)
from typing import Optional, Union

class AllelePopulation(BaseModel, extra='forbid'): 
    population: str
    alleleFrequency: str
    alleleCount: Optional[str]
    alleleCountHomozygous: Optional[str]
    alleleCountHeterozygous: Optional[str]
    alleleCountHemizygous: Optional[str]
    alleleNumber: Optional[str]

class GenotypePopulation(BaseModel, extra='forbid'): 
    population: str
    alleleFrequency: str
    alleleCount: Optional[str]
    genotypeHomozygous: Optional[str]
    genotypeHeterozygous: Optional[str]
    genotypeHemizygous: Optional[str]
    alleleNumber: Optional[str]

class GenotypePopulations(BaseModel, extra='forbid'): 
    numberOfPopulations: int
    source: str
    sourceReference: str
    populations: list[GenotypePopulation]

class AllelePopulations(BaseModel, extra='forbid'): 
    numberOfPopulations: int
    source: str
    sourceReference: str
    populations: list[AllelePopulation]