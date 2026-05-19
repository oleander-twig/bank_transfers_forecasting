import asyncio
from contextlib import asynccontextmanager

import numpy as np
from fastapi import FastAPI

from config import settings
from database import close_pool, fetch_history, fetch_profiles
from features import transform_data_for_prediction
from model import load_model_from_s3
from schemas import PredictRequest, PredictResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model_from_s3()
    yield
    await close_pool()


app = FastAPI(title="Bank Forecasting Service", lifespan=lifespan)


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    df, prof = await asyncio.gather(
        fetch_history(request.inn_list),
        fetch_profiles(request.inn_list),
    )

    inns = sorted(request.inn_list)
    n_start_week = int(df["week"].max())
    horizons = settings.forecast_weeks

    X = transform_data_for_prediction(df, prof, inns, n_start_week, horizons)

    pred_log = app.state.model.predict(X)
    pred = np.maximum(0, np.expm1(pred_log))

    results = []
    for i, inn_id in enumerate(inns):
        for h in range(1, horizons + 1):
            results.append(
                {
                    "inn_id": int(inn_id),
                    "week": n_start_week + h - 1,
                    "value": float(pred[i * horizons + h - 1]),
                }
            )

    return PredictResponse(predictions=results)
