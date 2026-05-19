from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/bank_forecasting"
    s3_bucket: str = ""
    s3_model_key: str = "my_model.joblib"
    s3_endpoint_url: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "ru-central1"
    forecast_weeks: int = 12

    class Config:
        env_file = ".env"


settings = Settings()
