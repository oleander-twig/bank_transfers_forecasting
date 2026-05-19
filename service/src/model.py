import io

import boto3
from botocore.client import Config
import joblib

from config import settings


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
