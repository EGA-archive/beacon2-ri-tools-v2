import json
import argparse
from pydantic import (
    BaseModel,
    ValidationError,
    PrivateAttr
)

class AllelePopulation(BaseModel, extra='forbid'):
    population: str
    alleleFrequency: str
    alleleCount: str | None = ""
    alleleCountHomozygous: str | None = ""
    alleleCountHeterozygous: str | None = ""
    alleleCountHemizygous: str | None = ""
    alleleNumber: str | None = ""

class GenotypePopulation(BaseModel, extra='forbid'):
    population: str
    alleleFrequency: str
    alleleCount: str | None = ""
    genotypeHomozygous: str | None = ""
    genotypeHeterozygous: str | None = ""
    genotypeHemizygous: str | None = ""
    alleleNumber: str | None = ""

class GenotypePopulations(BaseModel, extra='forbid'):
    source: str
    sourceReference: str
    populations: list[GenotypePopulation]

class AllelePopulations(BaseModel, extra='forbid'):
    source: str
    sourceReference: str
    populations: list[AllelePopulation]
