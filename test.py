
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


#iterate over a S3 bucket and moves files from 
# one to another the specific folder in another bucket
# and tag them with the new bucket name
def copy_files(source_bucket, destination_bucket, source_prefix, destination_prefix):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(source_bucket)
    for obj in bucket.objects.filter(Prefix=source_prefix):
        #print(obj.key)
        copy_source = {
            'Bucket': source_bucket,
            'Key': obj.key
        }
        new_key = obj.key.replace(source_prefix, destination_prefix)
        s3.meta.client.copy(copy_source, destination_bucket, new_key)
        #add metadata to the file
        s3.meta.client.put_object_tagging(
            Bucket=destination_bucket,
            Key=new_key,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'processID',
                        'Value': str(uuid.uuid4())
                    },
                ]
            }
        )
        #delete the file from the source bucket
        s3.Object(source_bucket, obj.key).delete()
        print(f"Moved {obj.key} to {destination_bucket} bucket.")