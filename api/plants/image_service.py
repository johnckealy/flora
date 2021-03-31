import boto3
from boto3 import session as sn
from botocore.client import Config
from boto3.s3.transfer import S3Transfer
import io

#Use the API Keys you generated at Digital Ocean
ACCESS_ID = 'U6IF3BBW2NOWZYMVJFMP'
SECRET_KEY = '+wp3eSbtorFE6FqvowkdefjAwC4MqqiYgfgHzOzbZTY'
DOSPACES_BASE_URL = 'https://floraimages.nyc3.digitaloceanspaces.com'
DOSPACES_REGION = 'nyc3'



def image_service(file_obj, bucket, filename):
    session = sn.Session()
    client = session.client(
        's3',
        region_name=DOSPACES_REGION,
        endpoint_url=DOSPACES_BASE_URL,
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=SECRET_KEY
    )

    file_obj.seek(0)
    client.upload_fileobj(file_obj, bucket, filename, ExtraArgs={'ACL': 'public-read'})

    return f"{DOSPACES_BASE_URL}/{bucket}/{filename}"
