import os
import io
import sys
import json
# from main import use_model

def lambda_handler(event, context):
    # TODO implement
    print(f"(print) In the Python Lambda, bucketname is {os.environ.get('BUCKETNAME')}")

    try:
        print("Importing torch...")
        import torch
        print("Imported torch!!!")
    except Exception as e:
        print('Exception str: '+ str(e))
        print('Exception repr: '+ str(e))
        return {
            'statusCode': 200,
            'body': json.dumps(f"Well that didn't go well")
        }

    # if torch.cuda.is_available():
    #     device = torch.device("cuda:0")
    #     print("Running on the GPU")
    # else:
    #     device = torch.device("cpu")
    #     print("Running on the CPU")

    # with open("./model-2021-01-06_16.57.31.pt", "rb") as state_dict_file:
    #     bytes_io = io.BytesIO(state_dict_file.read())
    #     use_model(bytes_io, './10017.jpg', device)

    return {
        'statusCode': 200,
        'body': json.dumps(f"(json) In the Python Lambda, bucketname is {os.environ.get('BUCKETNAME')}")
    }

if __name__ == '__main__':
    lambda_handler(None, None)