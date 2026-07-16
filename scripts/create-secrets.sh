#!/bin/bash
# Script to initialize resources in ministack for the project

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

# Create secrets manager
if aws --endpoint-url=$AWS_ENDPOINT_URL secretsmanager describe-secret --secret-id dip-secrets 2>/dev/null; then
    echo "Secrets already exist: dip-secrets"
else
    secrets=$(jq -R -s 'split("\n") | map(select(length > 0 and (startswith("#") | not))) | map(split("=")) | map({(.[0]): .[1]}) | add' < ./.env)
    aws --endpoint-url=$AWS_ENDPOINT_URL secretsmanager create-secret --name dip-secrets --secret-string "$secrets"
    echo "Successfully created secrets: dip-secrets"
fi