import pytest
from pydantic import ValidationError
from validators.analyses import Analyses


def test_analyses_valid_date():
    analysis = Analyses(
        id="A1",
        pipelineName="test-pipeline",
        analysisDate="2024-01-01T12:00:00Z",
    )
    assert analysis.analysisDate == "2024-01-01T12:00:00Z"


def test_analyses_invalid_date_raises():
    with pytest.raises(ValidationError):
        Analyses(
            id="A2",
            pipelineName="test-pipeline",
            analysisDate="definitely-not-a-date",
        )
