from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    inn_list: list[str] = Field(..., min_length=1, description="Список ИНН клиентов")


class PredictionItem(BaseModel):
    inn_id: str
    week: int
    value: float


class PredictResponse(BaseModel):
    predictions: list[PredictionItem]
