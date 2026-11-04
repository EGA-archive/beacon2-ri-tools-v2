from pydantic import BaseModel, PrivateAttr


class Analyses(BaseModel, extra='allow'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: str | None = PrivateAttr()
    aligner: str | None = None
    analysisDate: str
    biosampleId: str | None = None
    id: str
    individualId: str | None = None
    info: dict | None = None
    pipelineName: str
    pipelineRef: str | None=None
    runId: str | None=None
    variantCaller: str | None=None

