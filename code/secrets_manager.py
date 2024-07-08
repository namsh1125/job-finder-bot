import json
import boto3
from botocore.exceptions import ClientError

def get_secret_values(secret_name, region_name):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        
        saramin_api_key = secret.get('saramin_api_key')
        job_info = secret.get('job_info', {})
        
        return saramin_api_key, job_info
        
    except ClientError as e:
        raise e