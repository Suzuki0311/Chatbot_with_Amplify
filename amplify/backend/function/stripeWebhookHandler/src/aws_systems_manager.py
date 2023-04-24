import boto3
from botocore.exceptions import ClientError

# AWS region name
AWS_REGION = "ap-northeast-1"


def get_secret(secret_key):
    try:
        # Create a client for AWS Systems Manager
        ssm = boto3.client('ssm', region_name=AWS_REGION)

        # Get the secret from AWS SSM
        response = ssm.get_parameter(
            Name=secret_key,
            WithDecryption=True
        )

        # Return the value of the secret
        return response['Parameter']['Value']
    except ClientError as e:
        raise e