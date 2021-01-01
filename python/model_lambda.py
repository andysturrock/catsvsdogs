import os
import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(f"In the Python Lambda, bucketname is {os.environ.get('BUCKETNAME')}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def run_model(event, context):
    from main import use_model
    pass

