from pydantic import BaseModel

class PredictionRequest(BaseModel):
    kindb: str
    kindc: str

class PredictionResponse(BaseModel):
    kindb: str
    kindc: str
    predictedLoseRate: float
    similarCaseTotal: int
    similarCaseLost: int