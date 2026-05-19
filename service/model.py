import io

import boto3
from botocore.client import Config
import joblib
import numpy as np
import pandas as pd

from config import settings
from features import build_features_from_pivot


def load_model_from_s3():
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url or None,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )
    buf = io.BytesIO()
    s3.download_fileobj(settings.s3_bucket, settings.s3_model_key, buf)
    buf.seek(0)
    return joblib.load(buf)


def predict_recursive(
    model,
    pivot: pd.DataFrame,
    start_week: int,
    n_weeks: int,
) -> list[dict]:
    """Run recursive 12-week forecast.

    For each week, builds features from the pivot (which includes all prior
    predictions), predicts in log-space, inverse-transforms, and appends
    the prediction back into the pivot for subsequent weeks.

    Returns list of dicts: {inn_id, week, value}.
    """
    pivot = pivot.copy()
    results: list[dict] = []

    for offset in range(n_weeks):
        tw = start_week + offset
        x_week = build_features_from_pivot(pivot, tw)
        pred_log = model.predict(x_week)
        pred = np.maximum(0, np.expm1(pred_log))

        pivot[tw] = pred

        for inn_id, value in zip(pivot.index, pred):
            results.append({"inn_id": int(inn_id), "week": tw, "value": float(value)})

    return results
