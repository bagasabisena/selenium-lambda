import json
import time

import boto3

with open('config.json') as f:
    config = json.load(f)

role_arn = None
if 'role_arn' in config:
    if config['role_arn']:
        role_arn = config['role_arn']

if not role_arn:
    role_name = f'SeleniumLambdaRole-{config["project_name"]}'
    assume_role_policy_doc = '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
    print(f'creating default role {role_name}')
    client = boto3.client('iam')
    try:
        response = client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy_doc,
            Description=f'automatically created by selenium-lambda template for lambda function {config["project_name"]}',
        )
    except client.exceptions.EntityAlreadyExistsException:
        print(f'default role {role_name} already exists')
        arn = client.get_role(RoleName=role_name)['Role']['Arn']
    else:
        arn = response['Role']['Arn']
        # attach policy
        print('attaching policy AWSLambdaFullAccess')
        response = client.attach_role_policy(
            PolicyArn='arn:aws:iam::aws:policy/AWSLambdaFullAccess',
            RoleName=role_name,
        )

    config['role_arn'] = arn

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    # allow several seconds to ensure that the role is created
    # https://stackoverflow.com/questions/36419442/the-role-defined-for-the-function-cannot-be-assumed-by-lambda
    time.sleep(10)
    
    exit(0)
else:
    print(f'use existing role ARN {role_arn}')
    print('this program won\'t check if the role is actually fit for lambda usage')
    print('it\'s your responsibility to ensure that the role is setup for lambda')
    exit(0)
    