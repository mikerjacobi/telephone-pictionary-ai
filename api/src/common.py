from dataclasses import dataclass
import boto3
import botocore
from openai import OpenAI


@dataclass
class AppContext:
    s3: botocore.client.BaseClient
    # dynamodb: botocore.client.BaseClient
    openai: OpenAI
    env: str = "sandbox"
    image_bucket_name: str = "telephone-pictionary-sandbox"
