import sys

import argparse

import json

from schemas.commons import (ontologyTerm, timeInterval, measurementVal, quantity)

parser = argparse.ArgumentParser()

#diseases
parser.add_argument("-dis", "--diseases", action='store_true')
parser.add_argument("-dco", "--diseaseCode")
parser.add_argument("-aoo", "--ageOfOnset")
parser.add_argument("-fmh", "--familyHistory", action='store_true')
parser.add_argument("-not", "--notes", action='store_true')
parser.add_argument("-sev", "--severity")
parser.add_argument("-sta", "--stage")

#ethnicity
parser.add_argument("-eth", "--ethnicity")

#exposures
parser.add_argument("-exp", "--exposures", action='store_true')
parser.add_argument("-eco", "--exposureCode")
parser.add_argument("-uni", "--unit")
parser.add_argument("-dat", "--date", action='store_true')
parser.add_argument("-val", "--value", action='store_true')

#geographicOrigin
parser.add_argument("-geo", "--geographicOrigin")

#info
parser.add_argument("-inf", "--info", action='store_true')

#interventionsOrProcedures
parser.add_argument("-iop", "--interventionsOrProcedures", action='store_true')
parser.add_argument("-aap", "--ageAtProcedure")
parser.add_argument("-bsi", "--bodySite")
parser.add_argument("-dop", "--dateOfProcedure", action='store_true')
parser.add_argument("-pco", "--procedureCode")

#karyotypicSex
parser.add_argument("-kar", "--karyotypicSex", action='store_true')

#measures
parser.add_argument("-mea", "--measures", action='store_true')
parser.add_argument("-aco", "--assayCode")
parser.add_argument("-mva", "--measurementValue")
parser.add_argument("-nom", "--notesm", action='store_true')
parser.add_argument("-obm", "--observationMoment")
parser.add_argument("-pro", "--procedure", action='store_true')
parser.add_argument("-map", "--ageAtProcedurem")
parser.add_argument("-msi", "--bodySitem")
parser.add_argument("-mop", "--dateOfProcedurem", action='store_true')
parser.add_argument("-mco", "--procedureCodem")
parser.add_argument("-datm", "--measuresDate", action='store_true')

#pedigrees
parser.add_argument("-ped", "--pedigrees", action='store_true')
parser.add_argument("-pedco", "--diseaseCodep")
parser.add_argument("-peaoo", "--ageOfOnsetp")
parser.add_argument("-pefmh", "--familyHistoryp", action='store_true')
parser.add_argument("-penot", "--notesp", action='store_true')
parser.add_argument("-pesev", "--severityp")
parser.add_argument("-pesta", "--stagep")
parser.add_argument("-nsu", "--numSubjects", action='store_true')

#phenotypicFeatures
parser.add_argument("-phe", "--phenotypicFeatures", action='store_true')
parser.add_argument("-fet", "--featureType")
parser.add_argument("-evi", "--evidence", action='store_true')
parser.add_argument("-evc", "--evidenceCode")
parser.add_argument("-ref", "--reference", action='store_true')
parser.add_argument("-exc", "--excluded", action='store_true')
parser.add_argument("-mod", "--modifiers", action='store_true')
parser.add_argument("-phenotes", "--phenotes", action='store_true')
parser.add_argument("-ons", "--onset")
parser.add_argument("-res", "--resolution")
parser.add_argument("-phenosev", "--phenoseverity")

#sex
parser.add_argument("-sex", "--sex", action='store_true')

#treatments
parser.add_argument("-tre", "--treatments", action='store_true')
parser.add_argument("-tco", "--treatmentCode")
parser.add_argument("-taao", "--ageAtOnset")
parser.add_argument("-cdo", "--cumulativeDose")
parser.add_argument("-doi", "--doseInterval", action='store_true')
parser.add_argument("-doii", "--doseIntervali")
parser.add_argument("-doiq", "--doseIntervalq")
parser.add_argument("-dois", "--doseIntervals")
parser.add_argument("-roa", "--routeOfAdministration")

args = parser.parse_args()

individuals = {}

individuals['id']=""
individuals['sex']={"id":""}

if args.sex == True:
    individuals['sex']={"id":"", "label": ""}

if args.diseases == True:
    individuals['diseases']={}
    dco = ontologyTerm(args.diseaseCode)
    individuals['diseases']['diseaseCode']= dco
    if args.ageOfOnset:
        aoo = timeInterval(args.ageOfOnset)
        individuals['diseases']['ageOfOnset'] = aoo
    if args.familyHistory == True:
        individuals['diseases']['familyHistory'] = ""
    if args.notes == True:
        individuals['diseases']['notes'] = ""
    if args.severity:
        sev = ontologyTerm(args.severity)
        individuals['diseases']['severity'] = sev
    if args.stage:
        sta = ontologyTerm(args.stage)
        individuals['diseases']['stage'] = sta
if args.ethnicity:
    individuals['ethnicity']={}
    eth = ontologyTerm(args.ethnicity)
    individuals['ethnicity']= eth
if args.exposures == True:
    individuals['exposures']={}
    individuals['exposures']['ageAtExposure']= {"iso8601duration":""}
    eco = ontologyTerm(args.exposureCode)
    individuals['exposures']['exposureCode']= eco
    individuals['exposures']['duration']= ""
    uni = ontologyTerm(args.unit)
    individuals['exposures']['unit']= eco
    if args.date == True:
        individuals['exposures']['date'] = ""
    if args.value == True:
        individuals['exposures']['value'] = ""
if args.geographicOrigin:
    individuals['geographicOrigin']={}
    geo = ontologyTerm(args.geographicOrigin)
    individuals['geographicOrigin']= geo
if args.info:
    individuals['info']={}
if args.interventionsOrProcedures:
    individuals['interventionsOrProcedures']={}
    pco = ontologyTerm(args.procedureCode)
    individuals['interventionsOrProcedures']['procedureCode'] = pco
    if args.ageAtProcedure:
        aap = timeInterval(args.ageAtProcedure)
        individuals['interventionsOrProcedures']['ageAtProcedure'] = aap
    if args.bodySite:
        bsi = ontologyTerm(args.bodySite)
        individuals['interventionsOrProcedures']['bodySite'] = bsi
    if args.dateOfProcedure:
        individuals['interventionsOrProcedures']['dateOfProcedure'] = ""
if args.karyotypicSex == True:
    individuals['karyotypicSex']=""
if args.measures == True:
    individuals['measures']={}
    aco = ontologyTerm(args.assayCode)
    individuals['measures']['assayCode']= aco
    mva = measurementVal(args.measurementValue)
    individuals['measures']['measurementValue']= mva
    if args.notesm == True:
        individuals['measures']['notes'] = ""
    if args.measuresDate == True:
        individuals['measures']['date'] = ""
    if args.observationMoment:
        obm = timeInterval(args.observationMoment)
        individuals['measures']['observationMoment'] = obm
    if args.procedure:
        individuals['measures']['procedure'] = {}
        mco = ontologyTerm(args.procedureCodem)
        individuals['measures']['procedure']['procedureCode'] = mco
        if args.ageAtProcedurem:
            map = timeInterval(args.ageAtProcedure)
            individuals['measures']['procedure']['ageAtProcedure'] = map
        if args.bodySitem:
            msi = ontologyTerm(args.bodySite)
            individuals['measures']['procedure']['bodySite'] = msi
        if args.dateOfProcedurem:
            individuals['measures']['procedure']['dateOfProcedure'] = ""
if args.pedigrees == True:
    individuals['pedigrees']={}
    individuals['pedigrees']['disease']={}
    pedco = ontologyTerm(args.diseaseCodep)
    individuals['pedigrees']['disease']['diseaseCode']= pedco
    if args.ageOfOnsetp:
        peaoo = timeInterval(args.ageOfOnsetp)
        individuals['pedigrees']['disease']['ageOfOnset'] = peaoo
    if args.familyHistoryp == True:
        individuals['pedigrees']['disease']['familyHistory'] = ""
    if args.notesp == True:
        individuals['pedigrees']['disease']['notes'] = ""
    if args.severityp:
        pesev = ontologyTerm(args.severityp)
        individuals['pedigrees']['disease']['severity'] = pesev
    if args.stagep:
        pesta = ontologyTerm(args.stagep)
        individuals['pedigrees']['disease']['stage'] = sta
    individuals['pedigrees']['id']=""
    individuals['pedigrees']['members']=[]
    if args.numSubjects == True:
        individuals['pedigrees']['numSubjects']=[]
if args.phenotypicFeatures == True:
    individuals['phenotypicFeatures']={}
    fet = ontologyTerm(args.featureType)
    individuals['phenotypicFeatures']['featureType']=fet
    if args.evidence == True:
        individuals['phenotypicFeatures']['evidence']={}
        evc = ontologyTerm(args.evidenceCode)
        individuals['phenotypicFeatures']['evidence']['evidenceCode']=evc
        if args.reference == True:
            individuals['phenotypicFeatures']['evidence']['reference']['id']=""
            individuals['phenotypicFeatures']['evidence']['reference']['notes']=""
            individuals['phenotypicFeatures']['evidence']['reference']['reference']=""
    if args.excluded == True:
        individuals['phenotypicFeatures']['excluded']=""
    if args.modifiers == True:
        individuals['phenotypicFeatures']['modifiers']=[]
    if args.phenotes == True:
        individuals['phenotypicFeatures']['notes']=""
    if args.onset:
        individuals['phenotypicFeatures']['onset']={}
        ons = timeInterval(args.onset)
        individuals['phenotypicFeatures']['onset']=ons
    if args.resolution:
        individuals['phenotypicFeatures']['resolution']={}
        res = timeInterval(args.resolution)
        individuals['phenotypicFeatures']['resolution']=res
    if args.phenoseverity:
        individuals['phenotypicFeatures']['severity']={}
        phenosev = ontologyTerm(args.phenoseverity)
        individuals['phenotypicFeatures']['severity']=phenosev
if args.treatments == True:
    individuals['treatments']={}
    tco = ontologyTerm(args.treatmentCode)
    individuals['treatments']['treatmentCode']=tco
    if args.ageAtOnset:
        individuals['treatments']['ageAtOnset']={}
        taao = ontologyTerm(args.ageAtOnset)
        individuals['treatments']['ageAtOnset']=taao
    if args.cumulativeDose:
        individuals['treatments']['cumulativeDose']={}
        cdo = quantity(args.cumulativeDose)
        individuals['treatments']['cumulativeDose']=cdo
    if args.doseInterval:
        individuals['treatments']['doseInterval']={}
        doii = timeInterval(args.doseIntervali)
        doiq = quantity(args.doseIntervalq)
        dois = ontologyTerm(args.doseIntervals)
        individuals['treatments']['doseInterval']['interval']=doii
        individuals['treatments']['doseInterval']['quantity']=doiq
        individuals['treatments']['doseInterval']['scheduleFrequency']=dois
    if args.routeOfAdministration:
        individuals['treatments']['routeOfAdministration']={}
        roa = ontologyTerm(args.routeOfAdministration)
        individuals['treatments']['routeOfAdministration']=roa
    









with open('individuals/individuals.json', 'w', encoding='utf-8') as f:
    json.dump(individuals, f, ensure_ascii=False, indent=4)


    
