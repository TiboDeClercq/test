#write some unit test for the file python.py


import unittest
import boto3
import json
import uuid
from moto import mock_s3
from python import Python
from botocore.exceptions import ClientError
from unittest.mock import patch


class TestPython(unittest.TestCase):
    def test_generate_uuid(self):
        #setup
        python = Python()
        #act
        result = python.generate_uuid()
        #assert
        self.assertEqual(type(result), str)
        self.assertEqual(len(result), 36)
        
        
    @mock_s3
    def test_upload_file(self):
        #setup
        python = Python()
        bucket_name = 'test-bucket'
        subsystem = 'test-subsystem'
        project = 'test-project'
        textract_process = 'test-textract'
        file_name = 'test-file'
        file_path = 'test-path'
        python.s3_client.create_bucket(Bucket=bucket_name)
        #act
        python.upload_file(file_name, file_path, bucket_name, subsystem, project, textract_process)
        #assert
        self.assertEqual(python.s3_client.head_bucket(Bucket=bucket_name), None)
        
        
    def test_check_textract_service(self):
        #setup
        python = Python()
        #act
        result = python.check_textract_service('textract')
        #assert
        self.assertEqual(result, 'textract')
        
        
    def test_check_textract_service_exception(self):
        #setup
        python = Python()
        #act
        result = python.check_textract_service('textract')
        #assert
        self.assertEqual(result, 'textract')
        
        
    def test_check_textract_service_exception(self):
        #setup
        python = Python()
        #act
        result = python.check_textract_service('textract')
        #assert
        self.assertEqual(result, 'textract')
        
