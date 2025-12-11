import pytest
from pydantic import ValidationError
from validators.ontology_term import OntologyTerm

@pytest.mark.parametrize("curie,label", [
    ("NCIT:C20197", "male"),
    ("HP:0000118", "Phenotypic abnormality"),
    ("EFO:0000400", None),
])
def test_valid_curie_formats(curie, label):
    term = OntologyTerm(id=curie, label=label)
    assert term.id == curie
    assert term.label == label


def test_invalid_ontologyterm():
    with pytest.raises(ValidationError):
        OntologyTerm(
            id="male",
            label="NCIT:C20197",
        )

@pytest.mark.parametrize("bad_id", [
    "NCITC20197",    # missing colon
    "NCIT:",         # nothing after colon
    ":C20197",       # nothing before colon
    "NCIT:C-20197",  # dash not allowed by your regex
    "NCIT C20197",   # space
])
def test_invalid_curie_formats(bad_id):
    with pytest.raises(ValidationError):
        OntologyTerm(id=bad_id, label="test label")


def test_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        OntologyTerm(
            id="NCIT:C20197",
            label="male",
            extra_field="nope",
        )

def test_id_must_be_string():
    with pytest.raises(ValidationError):
        OntologyTerm(id=123, label="number")
