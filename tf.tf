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
# Configure AWS provider
provider "aws" {
  region = "us-east-1"
}

# Create an ECR repository for the Docker image
resource "aws_ecr_repository" "example_ecr_repo" {
  name = "example-ecr-repo"
}

# Build and push the Docker image to the ECR repository
resource "docker_image" "example_docker_image" {
  name          = "example-docker-image"
  build         = "./docker"
  registry_auth = aws_ecr_registry.example_ecr_registry.authorization_token
}

# Create an ECR registry to authorize the Lambda function to access the Docker image
resource "aws_ecr_registry" "example_ecr_registry" {
  depends_on = [aws_ecr_repository.example_ecr_repo]
}

# Create an IAM role for the Lambda function
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

# Create an IAM policy for the Lambda function to access the Docker image
resource "aws_iam_policy" "example_lambda_policy" {
  name        = "example_lambda_policy"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = aws_ecr_repository.example_ecr_repo.arn
      }
    ]
  })
}

# Attach the IAM policy to the Lambda function role
resource "aws_iam_role_policy_attachment" "example_lambda_policy_attachment" {
  policy_arn = aws_iam_policy.example_lambda_policy.arn
  role       = aws_iam_role.example_lambda_role.name
}

# Create the Lambda function using the Docker image and a layer
resource "aws_lambda_function" "example_lambda" {
  function_name = "example-lambda-function"
  role         = aws_iam_role.example_lambda_role.arn
  handler      = "lambda_function.handler"
  runtime      = "provided.al2"
  layers       = [aws_lambda_layer_version.example_layer.arn]

  # Environment variables
  environment {
    variables = {
      EXAMPLE_VAR = "example-value"
    }
  }

  # Function code
  image_uri = docker_image.example_docker_image.latest
}

# Create a Lambda layer version
resource "aws_lambda_layer_version" "example_layer" {
  layer_name = "example-layer"
  filename   = "layer.zip"
  compatible_runtimes = [
    "python3.9",
    "provided.al2"
  ]

  # Build and package the layer contents
  source_code_hash = filebase64sha256("layer.zip")
}

