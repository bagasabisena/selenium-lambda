import json
import os

import boto3

with open('config.json') as f:
    config = json.load(f)

package_bucket = None
if 'package_bucket' in config:
    if config['package_bucket']:
        package_bucket = config['package_bucket']

package_key = None
if 'package_key' in config:
    if config['package_key']:
        package_key = config['package_key']

if not package_bucket:
    print('You must supply "package_bucket" config. This is the bucket where the zipped function is deployed. You must create the bucket yourself')
    exit(1)

if not package_key:
    print('you must supply "package_key" config. This is the S3 key which the zip is named')
    exit(1)

s3 = boto3.resource('s3')

bucket = s3.Bucket(package_bucket)
print('uploading build.zip to S3')
uploaded = 0
total = os.path.getsize('build.zip')

def upload_progress(bytes_):
    if bytes_ == 0:
        return
    
    global uploaded
    uploaded += bytes_
    progress = int(uploaded / total * 100)
    print("\r", f"{progress}%", end='')

bucket.upload_file(
    Filename='build.zip',
    Key=package_key,
    Callback=upload_progress
)

print('\nfinish uploading')
