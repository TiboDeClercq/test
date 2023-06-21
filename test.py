def copy_files(source_bucket, destination_bucket, source_prefix, destination_prefix):
    
    #create s3 resource
    s3 = boto3.client('s3')
    
    #get the list of files in the source bucket
    #with the source prefix
    source_files = s3.list_objects(Bucket=source_bucket, Prefix=source_prefix)

    #loop through the list of files
    for file in source_files['Contents']:
        #get the name of the file
        file_name = file['Key']

        #create the destination file name
        destination_file_name = file_name.replace(source_prefix, destination_prefix)

        #copy the file to the destination bucket
        s3.copy_object(Bucket=destination_bucket, 
                       CopySource={'Bucket': source_bucket, 'Key': file_name}, 
                       Key=destination_file_name)

        #tag the file with the new bucket name
        s3.put_object_tagging(Bucket=destination_bucket, 
                              Key=destination_file_name,
                              Tagging={'TagSet': [{'Key': 'Bucket', 'Value': destination_bucket}]})

        #delete the file from the source bucket
        s3.delete_object(Bucket=source_bucket, Key=file_name)