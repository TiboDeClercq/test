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
