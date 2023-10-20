import json

def ontologyTerm(dc):
    data = {}
    if dc == 'ontology':
        data = {"id":""}
    elif dc == 'ontologyl':
        data = {"id":"", "label": ""}
    return data

def timeInterval(aoo):
    data={}
    if aoo == 'age':
        data = {"iso8601duration":""}
    elif aoo == 'rangeinterval':
        data = {"start":"", "end": ""}
    elif aoo == 'gestationald':
        data = {"days":""}
    elif aoo == 'timestamp':
        data = ""
    elif aoo == 'ontology':
        data = {"id":""}
    elif aoo == 'ontologyl':
        data = {"id":"", "label": ""}
    return data

def measurementVal(measurementValue):
    data = {}
    if measurementValue == 'ontology':
        data = {"id":""}
    elif measurementValue == 'ontologyl':
        data = {"id":"", "label": ""}
    elif measurementValue == 'unit':
        data = {"unit": {"id": ""},"value":""}
    elif measurementValue == 'unitl':
        data = {"unit": {"id": "", "label": ""},"value":""}
    elif measurementValue == 'referenceRangeu':
        data = {"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": ""},"value":""}
    elif measurementValue == 'referenceRangeul':
        data = {"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": "", "label":""},"value":""}
    elif measurementValue == 'referenceRangelu':
        data = {"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label": ""}}, "unit": {"id": ""},"value":""}
    elif measurementValue == 'referenceRangelul':
        data = {"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label": ""}}, "unit": {"id": "", "label": ""},"value":""}
    elif measurementValue == 'typedQuantitiesuu':
        data = [{"TypedQuantity":{"unit": {"id": ""},"value":""}},{"quantityType":{"id":""}}]
    elif measurementValue == 'typedQuantitiesuul':
        data = [{"TypedQuantity":{"unit": {"id": ""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif measurementValue == 'typedQuantitiesulul':
        data = [{"TypedQuantity":{"unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif measurementValue == 'typedQuantitiesulu':
        data = [{"TypedQuantity":{"unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":""}}]
    elif measurementValue == 'typedQuantitiesruu':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": ""},"value":""}},{"quantityType":{"id":""}}]
    elif measurementValue == 'typedQuantitiesrluu':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label": ""}}, "unit": {"id": ""},"value":""}},{"quantityType":{"id":""}}]
    elif measurementValue == 'typedQuantitiesrulu':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":""}}]
    elif measurementValue == 'typedQuantitiesruul':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": ""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif measurementValue == 'typedQuantitiesrlulu':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label":""}}, "unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":""}}]
    elif measurementValue == 'typedQuantitiesrlulul':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label":""}}, "unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif measurementValue == 'typedQuantitiesrulul':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif measurementValue == 'typedQuantitiesrluul':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label":""}}, "unit": {"id": ""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    return data

def quantity(cumulativeDose):
    data = {}
    if cumulativeDose == 'ontology':
        data = {"id":""}
    elif cumulativeDose == 'ontologyl':
        data = {"id":"", "label": ""}
    elif cumulativeDose == 'unit':
        data = {"unit": {"id": ""},"value":""}
    elif cumulativeDose == 'unitl':
        data = {"unit": {"id": "", "label": ""},"value":""}
    elif cumulativeDose == 'referenceRangeu':
        data = {"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": ""},"value":""}
    elif cumulativeDose == 'referenceRangeul':
        data = {"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": "", "label":""},"value":""}
    elif cumulativeDose == 'referenceRangelu':
        data = {"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label": ""}}, "unit": {"id": ""},"value":""}
    elif cumulativeDose == 'referenceRangelul':
        data = {"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label": ""}}, "unit": {"id": "", "label": ""},"value":""}
    elif cumulativeDose == 'typedQuantitiesuu':
        data = [{"TypedQuantity":{"unit": {"id": ""},"value":""}},{"quantityType":{"id":""}}]
    elif cumulativeDose == 'typedQuantitiesuul':
        data = [{"TypedQuantity":{"unit": {"id": ""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif cumulativeDose == 'typedQuantitiesulul':
        data = [{"TypedQuantity":{"unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif cumulativeDose == 'typedQuantitiesulu':
        data = [{"TypedQuantity":{"unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":""}}]
    elif cumulativeDose == 'typedQuantitiesruu':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": ""},"value":""}},{"quantityType":{"id":""}}]
    elif cumulativeDose == 'typedQuantitiesrluu':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label": ""}}, "unit": {"id": ""},"value":""}},{"quantityType":{"id":""}}]
    elif cumulativeDose == 'typedQuantitiesrulu':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":""}}]
    elif cumulativeDose == 'typedQuantitiesruul':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": ""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif cumulativeDose == 'typedQuantitiesrlulu':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label":""}}, "unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":""}}]
    elif cumulativeDose == 'typedQuantitiesrlulul':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label":""}}, "unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif cumulativeDose == 'typedQuantitiesrulul':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": ""}}, "unit": {"id": "", "label":""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    elif cumulativeDose == 'typedQuantitiesrluul':
        data = [{"TypedQuantity":{"referenceRange":{"id":"","high":"", "low": "", "unit": {"id": "", "label":""}}, "unit": {"id": ""},"value":""}},{"quantityType":{"id":"", "label":""}}]
    return data