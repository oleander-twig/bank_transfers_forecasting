import boto3
from botocore.client import Config
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    #config=Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
)
s3.upload_file('my_model.joblib', 'bank-forecasting', 'my_model.joblib')
print('uploaded')