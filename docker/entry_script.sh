#!/bin/sh

echo "args = <$*>"

if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
    echo "No AWS_LAMBDA_RUNTIME_API"
    exec /usr/local/bin/aws-lambda-rie /usr/local/bin/python -m awslambdaric $1
else
    echo "AWS_LAMBDA_RUNTIME_API = ${AWS_LAMBDA_RUNTIME_API}"
    exec /usr/local/bin/python -m awslambdaric $1
fi