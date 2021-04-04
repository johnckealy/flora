from boto3 import session as sn
import os

#Use the API Keys you generated at Digital Ocean
def image_service(file_obj, bucket, filename):
    session = sn.Session()
    DOSPACES_BASE_URL = os.environ.get('DOSPACES_BASE_URL')
    client = session.client(
        's3',
        region_name=os.environ.get('DOSPACES_REGION'),
        endpoint_url=DOSPACES_BASE_URL,
        aws_access_key_id=os.environ.get('DOSPACES_ACCESS_ID'),
        aws_secret_access_key=os.environ.get('DOSPACES_SECRET_KEY'),
    )

    file_obj.seek(0)
    client.upload_fileobj(file_obj, bucket, filename, ExtraArgs={'ACL': 'public-read'})

    return f"{DOSPACES_BASE_URL}/{bucket}/{filename}"
