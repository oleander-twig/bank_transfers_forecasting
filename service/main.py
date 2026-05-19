from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException

from config import settings
from database import close_pool, fetch_history
from model import load_model_from_s3, predict_recursive
from schemas import PredictRequest, PredictResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model_from_s3()
    yield
    await close_pool()


app = FastAPI(title="Bank Forecasting Service", lifespan=lifespan)


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    df = await fetch_history(request.inn_list)

    if df.empty:
        raise HTTPException(status_code=404, detail="No data found for provided INN list")

    pivot = df.pivot(index="inn_id", columns="week", values="target").fillna(0)

    last_known_week = int(pivot.columns.max())
    start_week = last_known_week + 1

    results = predict_recursive(
        model=app.state.model,
        pivot=pivot,
        start_week=start_week,
        n_weeks=settings.forecast_weeks,
    )

    return PredictResponse(predictions=results)
