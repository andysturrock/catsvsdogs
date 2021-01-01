import os
import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(f"In the Copy to EFS Python Lambda, bucketname is {os.environ.get('BUCKETNAME')}")
    copy_site_packages_from_s3()

    return {
        'statusCode': 200,
        'body': json.dumps('site-packages installed from S3 to EFS')
    }

def copy_site_packages_from_s3():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.environ.get('BUCKETNAME'))
    print(f"Files in {os.environ.get('BUCKETNAME')}")
    for obj in bucket.objects.all():
        key = obj.key
        print(f"key = {key}")
