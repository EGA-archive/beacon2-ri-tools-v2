import json
from pathlib import Path
from validators.individuals import Individuals

DATA_DIR = Path(__file__).parent / "data"

def test_individuals_from_json_valid():
    # Load test JSON
    with (DATA_DIR / "individual1.json").open() as f:
        data = json.load(f)

    ind = Individuals(**data)

    # Basic checks
    assert ind.id == "idSubject1g2ww0546589078"
    assert ind.sex.id == "NCIT:C20197"
    assert ind.sex.label == "Male"

    assert ind.geographicOrigin is not None
    assert ind.geographicOrigin.id == "ISO3166:AO"
    assert ind.geographicOrigin.label == "Angola"
