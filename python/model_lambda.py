import os
import io
import sys
import json
# import torch
# from main import use_model

def lambda_handler(event, context):
    # TODO implement
    print(f"In the Python Lambda, bucketname is {os.environ.get('BUCKETNAME')}")

    AWS_LAMBDA_RUNTIME_API = os.environ['AWS_LAMBDA_RUNTIME_API']
    print(f"AWS_LAMBDA_RUNTIME_API = {AWS_LAMBDA_RUNTIME_API}")

    # if torch.cuda.is_available():
    #     device = torch.device("cuda:0")
    #     print("Running on the GPU")
    # else:
    #     device = torch.device("cpu")
    #     print("Running on the CPU")

    # with open("./model-2021-01-06_16.57.31.pt", "rb") as state_dict_file:
    #     bytes_io = io.BytesIO(state_dict_file.read())
    #     use_model(bytes_io, './10017.jpg', device)

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }

# if __name__ == '__main__':
#     lambda_handler(None, None)