#!/bin/bash
# Script to initialize resources in ministack for the project

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

# Create S3 bucket for raw document storage and make sure its idempotent
# (i.e. if it already exists, don't fail)
if aws --endpoint-url=$AWS_ENDPOINT_URL s3api head-bucket --bucket dip-documents 2>/dev/null; then
    echo "S3 bucket already exists: dip-documents"
else
    aws --endpoint-url=$AWS_ENDPOINT_URL s3 mb s3://dip-documents
    echo "Successfully created S3 bucket: dip-documents"
fi

# Create SQS queue for processing document ingestion
if aws --endpoint-url=$AWS_ENDPOINT_URL sqs get-queue-url --queue-name dip-document-ingestion-queue 2>/dev/null; then
    echo "SQS queue already exists: dip-document-ingestion-queue"
else
    aws --endpoint-url=$AWS_ENDPOINT_URL sqs create-queue --queue-name dip-document-ingestion-queue
    echo "Successfully created SQS queue: dip-document-ingestion-queue"
fi
