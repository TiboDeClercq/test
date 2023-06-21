
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
# one to another bucket
# and tag them with the new bucket name
def copy_files(source_bucket, destination_bucket, source_prefix, destination_prefix):

    #create s3 resource
    s3 = boto3.resource('s3')
    #get the source bucket
    source_bucket = s3.Bucket(source_bucket)
    #get the destination bucket
    destination_bucket = s3.Bucket(destination_bucket)
    
    #iterate over the source bucket
    for obj in source_bucket.objects.filter(Prefix=source_prefix):
        #copy the object
        destination_bucket.copy({'Bucket': source_bucket.name, 'Key': obj.key}, obj.key)
        #tag the object
        destination_bucket.Object(obj.key).Tagging().put(Tagging={'TagSet': [{'Key': 'bucket', 'Value': destination_bucket.name}]})

    print("Done")