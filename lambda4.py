import boto3

def lambda_handler(event, context):
    # Configure SQS and DynamoDB clients
    sqs = boto3.client('sqs')
    dynamodb = boto3.client('dynamodb')
    
    # Specify the SQS queue URL and DynamoDB table name
    queue_url = 'YOUR_SQS_QUEUE_URL'
    table_name = 'YOUR_DYNAMODB_TABLE_NAME'
    
    # Receive a message from SQS
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    
    # Check if a message was received
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        
        # Extract the message body
        body = message['Body']
        
        # Write the message to DynamoDB
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'message': {'S': body}
            }
        )
        
        # Delete the message from SQS
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        
        return {
            'statusCode': 200,
            'body': 'Message processed and stored in DynamoDB'
        }
    else:
        return {
            'statusCode': 204,
            'body': 'No messages in the queue'
        }

