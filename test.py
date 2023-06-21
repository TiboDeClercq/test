
import boto3
import uuid
import os
import botocore
from botocore.exceptions import ClientError
from botocore.client import Config
from botocore.client import ClientError
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import NoCredentialsError


#iterate over a S3 bucket and move the files from 
# one to another the specific folder in another bucket
# and tag them with the new bucket name
def copy_files(source_bucket, destination_bucket, source_prefix, destination_prefix):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(source_bucket)
    for obj in bucket.objects.filter(Prefix=source_prefix):
        copy_source = {
            'Bucket': source_bucket,
            'Key': obj.key
        }
        destination_key = obj.key.replace(source_prefix, destination_prefix, 1)
        s3.meta.client.copy(copy_source, destination_bucket, destination_key)
        s3.Object(destination_bucket, destination_key).put(Tagging='bucket=' + destination_bucket)
        s3.Object(source_bucket, obj.key).delete()