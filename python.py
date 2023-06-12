
import inspect
import re
import uuid
import boto3

#TODO error handeling

class TextractUploader:
    def __init__(self, role_arn, session_name):
        self.role_arn = role_arn
        self.session_name = session_name
        self.s3_client = self._create_s3_client()
        
    def _create_s3_client(self):
        sts_client = boto3.client('sts')
        #Assume the role
        response = sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.session_name
        )

        credentials = response['Credentials']
        access_key = credentials['AccessKeyId']
        secret_key = credentials['SecretAccessKey']
        session_token = credentials['SessionToken']

        return boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )
    
    
    def upload_file(self, file_name, file_path, bucket_name, subsystem, project, textract_process):
        file_name = file_name
        file_path = file_path
        bucket_name = bucket_name
        subsystem = subsystem  
        project = project    
        textract_process = textract_process
        
        #check if S3 bucket exists
        # if self.s3_client.head_bucket(Bucket=bucket_name):
        

        if _check_textract_service(textract_process):
            destination_path = f"s3://{bucket_name}/incoming/{subsystem}/{project}/{textract_process}/{file_name}"
            self.s3_client.upload_file(file_path, bucket_name, destination_path)

        
        # check if folder exists within a bucket, if not create that folder
        if not self.s3_client.list_objects(Bucket=bucket_name, Prefix=f"incoming/{subsystem}/"):
            self.s3_client.put_object(Bucket=bucket_name, Key=f"incoming/{subsystem}/")
            if not self.s3_client.list_objects(Bucket=bucket_name, Prefix=f"incoming/{subsystem}/{project}/"):
                self.s3_client.put_object(Bucket=bucket_name, Key=f"incoming/{subsystem}/{project}/")
                if not self.s3_client.list_objects(Bucket=bucket_name, Prefix=f"incoming/{subsystem}/{project}/{textract_process}/"):
                    self.s3_client.put_object(Bucket=bucket_name, Key=f"incoming/{subsystem}/{project}/{textract_process}/")
                    self.s3_client.upload_file(file_path, bucket_name, destination_path)


        
        
        # self.s3_client.upload_file(file_path, bucket_name, s3_key)

    #move files from one bucket to another
    def move_file(self, source_bucket, source_key, destination_bucket, destination_key):
        copy_source = {
            'Bucket': source_bucket,
            'Key': source_key
        }
        self.s3_client.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=destination_key)
        self.s3_client.delete_object(Bucket=source_bucket, Key=source_key)
        #add metadata to the file
        self.s3_client.put_object_tagging(
            Bucket=destination_bucket,
            Key=destination_key,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'processID',
                        'Value': str(uuid.uuid4())
                    },
                ]
            }
        )
        
        
        
    #generate a UUID
    def generate_uuid(self):
        return str(uuid.uuid4())
    

#print all functions from the textract client
def _check_textract_service(args):
    for name, data in inspect.getmembers(boto3.client('textract')):
        if name.startswith('_'):
            continue
        if inspect.ismethod(data):
            return True
        else:
            return False

#get source bucket and type of textract processed based on the object name
def _get_source_bucket_and_textract_type(object_name):
    source_bucket = object_name.split('/')[1]
    textract_type = object_name.split('/')[5]
    return source_bucket, textract_type

#query a dynomoDB table and return a list of dictionaries
def _query_table(table_name, key, value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key(key).eq(value)
    )
    return response['Items']