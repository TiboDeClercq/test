
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