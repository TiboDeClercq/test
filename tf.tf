# Configure AWS provider
provider "aws" {
  region = "us-east-1"
}

# Define Lambda function
resource "aws_lambda_function" "example_lambda" {
  function_name = "example-lambda-function"
  role         = aws_iam_role.example_lambda_role.arn
  handler      = "lambda_function.lambda_handler"
  runtime      = "python3.9"
  filename     = "lambda_function.zip"
  source_code_hash = filebase64sha256("lambda_function.zip")

  # Environment variables
  environment {
    variables = {
      EXAMPLE_VAR = "example-value"
    }
  }

  # Function code
  source_code_hash = filebase64sha256("lambda_function.zip")
}

# Define Lambda function IAM role
resource "aws_iam_role" "example_lambda_role" {
  name = "example_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attach Lambda function IAM policies to the role
resource "aws_iam_role_policy_attachment" "example_lambda_policy_attachment" {
  policy_arn = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/AmazonSESFullAccess",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
  ]
  role = aws_iam_role.example_lambda_role.name
}

# Create Lambda function deployment package
resource "archive_file" "lambda_function" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_function"
  output_path = "${path.module}/lambda_function.zip"
}

