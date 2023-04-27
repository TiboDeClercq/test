#lambda Queue encryption 

import boto3

sqs = boto3.client('sqs')
s3 = boto3.client('s3')
textract = boto3.client('textract')

queue_url = 'SQS_QUEUE_URL'
bucket_name = 'S3_BUCKET_NAME'

def lambda_handler(event, context):
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=0
    )
    
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        message_body = message['Body']
        message_attributes = message['MessageAttributes']
        
        # Get file from S3 bucket
        file_key = message_attributes['FileKey']['StringValue']
        file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = file_obj['Body'].read()
        
        # Send file to Textract
        response = textract.analyze_document(
            Document={
                'Bytes': file_content
            },
            FeatureTypes=['TABLES', 'FORMS']
        )
        
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        
        
def lambda_handler(event, context):
    # Get the S3 object key from the event
    s3_key = event['Records'][0]['s3']['object']['key']
    
    # Define the input and output S3 bucket names
    input_bucket = 'my-input-bucket'
    output_bucket = 'my-output-bucket'
    
    # Define the KMS customer master key ID
    cmk_id = 'arn:aws:kms:us-east-1:123456789012:key/abcd1234-5678-90ef-ghij-klmn1234abcd'
    
    # Create an S3 client and download the file
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=input_bucket, Key=s3_key)
    data = response['Body'].read()
    
    # Create a KMS client and encrypt the file data
    kms = boto3.client('kms')
    response = kms.encrypt(KeyId=cmk_id, Plaintext=data)
    ciphertext = response['CiphertextBlob']
    
    # Upload the encrypted file to the output S3 bucket
    new_key = os.path.join('encrypted', s3_key)
    response = s3.put_object(Bucket=output_bucket, Key=new_key, Body=ciphertext)
    
    # Return a success message
    return {
        'statusCode': 200,
        'body': 'File encrypted successfully'
    }
