import json
import pprint

import boto3

with open('config.json') as f:
    config = json.load(f)

function_name = config['function_arn']
package_bucket = config['package_bucket']
package_key = config['package_key']

client = boto3.client('lambda')
try:
    response = client.update_function_code(
        FunctionName=function_name,
        S3Bucket=package_bucket,
        S3Key=package_key,
    )
except Exception as e:
    print('upload function code failed')
    raise
else:
    keys = ['FunctionName', 'FunctionArn', 'CodeSize', 'Version', 'LastModified', 'LastUpdateStatus']
    pprint.pprint({k: response[k] for k in keys if k in response}, indent=2)
