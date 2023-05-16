import boto3

class S3ImageUploader:
    def __init__(self, role_arn, session_name):
        self.role_arn = role_arn
        self.session_name = session_name
        self.s3_client = self._create_s3_client()

    def _create_s3_client(self):
        sts_client = boto3.client("sts")

        # Assume the role
        response = sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.session_name
        )

        # Extract temporary credentials
        credentials = response["Credentials"]
        access_key = credentials["AccessKeyId"]
        secret_key = credentials["SecretAccessKey"]
        session_token = credentials["SessionToken"]

        # Create an S3 client using the assumed role's credentials
        return boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )

    def upload_image(self, file_path, bucket_name, key):
        try:
            self.s3_client.upload_file(file_path, bucket_name, key)
            print("Image uploaded successfully!")
        except Exception as e:
            print(f"Failed to upload image: {e}")

def move_file(source_bucket, destination_bucket, source_key, destination_key):
    s3_client = boto3.client("s3")

    try:
        # Copy the file to the destination bucket
        copy_source = {
            "Bucket": source_bucket,
            "Key": source_key
        }
        s3_client.copy_object(
            CopySource=copy_source,
            Bucket=destination_bucket,
            Key=destination_key
        )

        # Delete the file from the source bucket
        s3_client.delete_object(
            Bucket=source_bucket,
            Key=source_key
        )

        print("File moved successfully!")
    except Exception as e:
        print(f"Failed to move file: {e}")
