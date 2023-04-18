import boto3

def lambda_handler(event, context):
    # Get the S3 object key from the S3 event
    s3_bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_object_key = event['Records'][0]['s3']['object']['key']

    # Initialize the AWS clients for S3 and Textract
    s3_client = boto3.client('s3')
    textract_client = boto3.client('textract')

    # Fetch the S3 object
    s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)

    # Send the object content to Textract for analysis
    response = textract_client.analyze_document(Document={'Bytes': s3_object['Body'].read()})

    # Do something with the Textract response, such as sending it to an SNS topic or saving it to a database
    print(response)
