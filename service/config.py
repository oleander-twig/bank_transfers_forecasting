from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost:5432/bank_forecasting"
    s3_bucket: str = ""
    s3_model_key: str = "models/lgbm_final.pkl"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "ru-central1"
    forecast_weeks: int = 12

    class Config:
        env_file = ".env"


settings = Settings()
