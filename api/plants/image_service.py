from boto3 import session as sn
import os
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io


ACCEPTED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/svg+xml', 'image/gif']

def reduce_image(image):
    """Input is an InMemoryUploadedFile object.
    Output is a resized PIL image object."""
    img = Image.open(image)
    return img.resize((500, 500), Image.ANTIALIAS)


def convert_to_InMemoryUploadedFile(original_file_obj, resized_image):
    """Takes a PIL image object and returns an InMemoryUploadedFile object"""
    bytesIO_obj = io.BytesIO()
    resized_image.save(bytesIO_obj, format='JPEG')
    img_fileobj = InMemoryUploadedFile(
        file=bytesIO_obj,
        charset=original_file_obj.charset,
        field_name=original_file_obj.field_name,
        name=original_file_obj.name,
        content_type=original_file_obj.content_type,
        size=original_file_obj.size)
    return img_fileobj

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

    if file_obj.content_type not in ACCEPTED_FILE_TYPES:
        return { "error": "unrecognized file type"}

    resized_image = reduce_image(file_obj)
    resized_file_obj = convert_to_InMemoryUploadedFile(file_obj, resized_image)

    resized_file_obj.seek(0)
    client.upload_fileobj(resized_file_obj, bucket, filename, ExtraArgs={'ACL': 'public-read'})

    return f"{DOSPACES_BASE_URL}/{bucket}/{filename}"
