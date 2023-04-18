import boto3

def lambda_handler(event, context):
    # Initialize the AWS clients for SQS, S3 and Textract
    sqs_client = boto3.client('sqs')
    s3_client = boto3.client('s3')
    textract_client = boto3.client('textract')

    # Get the SQS message containing the S3 object key
    sqs_message = sqs_client.receive_message(QueueUrl='YOUR_SQS_QUEUE_URL')['Messages'][0]
    s3_object_key = sqs_message['Body']

    # Delete the SQS message
    sqs_client.delete_message(QueueUrl='YOUR_SQS_QUEUE_URL', ReceiptHandle=sqs_message['ReceiptHandle'])

    # Fetch the S3 object
    s3_bucket_name = 'YOUR_S3_BUCKET_NAME'
    s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)

    # Send the object content to Textract for analysis
    response = textract_client.analyze_document(Document={'Bytes': s3_object['Body'].read()})

    # Do something with the Textract response, such as sending it to an SNS topic or saving it to a database
    print(response)

