import json

def lambda_handler(event, context):
    # TODO implement
    print("In the Python Lambda")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }