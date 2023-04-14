import json
import boto3
import base64

def lambda_handler(event, context):
    # Get the base64-encoded image data from the API Gateway event
    image_data = event['body']
    
    # Decode the image data from base64
    image_bytes = base64.b64decode(image_data)
    
    # Create a Textract client
    textract_client = boto3.client('textract')
    
    # Call Textract to extract text from the image
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    
    # Get the text from the Textract response
    text = response['Blocks'][0]['Text']
    
    # Create a SageMaker runtime client
    sagemaker_client = boto3.client('runtime.sagemaker')
    
    # Define the input format for the SageMaker endpoint
    content_type = 'text/plain'
    
    # Call the SageMaker endpoint with the extracted text
    response = sagemaker_client.invoke_endpoint(
        EndpointName='example-endpoint-name', # Replace with your endpoint name
        ContentType=content_type,
        Body=text.encode('utf-8')
    )
    
    # Get the response from the SageMaker endpoint
    result = response['Body'].read().decode('utf-8')
    
    # Return the result as a JSON object
    return {
        'statusCode': 200,
        'body': json.dumps({'result': result})
    }
