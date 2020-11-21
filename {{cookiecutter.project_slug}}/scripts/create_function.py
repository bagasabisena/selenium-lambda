import json

import boto3

with open('config.json') as f:
    config = json.load(f)

function_arn = None
if 'function_arn' in config:
    if config['function_arn']:
        function_arn = config['function_arn']

if not function_arn:
    # aws lambda create-function \
	# 	--function-name $(PROJECT_NAME) \
	# 	--role $(TMP_ROLE_ARN) \
	# 	--runtime python3.7 \
	# 	--handler src.$(FUNCTION_HANDLER) \
	# 	--timeout $(FUNCTION_TIMEOUT) \
	# 	--memory-size $(FUNCTION_MEMORY_SIZE) \
	# 	--output text --query 'Arn' \
	# 	--zip-file fileb://build.zip \
	# 	--environment 'Variables={PATH=/var/task/bin,PYTHONPATH=/var/task/src:/var/task/lib}'
    project_name = config['project_name']
    role_arn = config['role_arn']
    function_handler = config['function_handler']
    timeout = config['function_timeout']
    memory_size = config['function_memory_size']
    # open build.zip, encode into bytes
    with open('build.zip', 'rb') as f:
        build_str = f.read()
    print(f'creating lambda function {project_name}')
    client = boto3.client('lambda')
    try:
        response = client.create_function(
            FunctionName=project_name,
            Runtime='python3.7',
            Role=role_arn,
            Handler=function_handler,
            Description='{{ cookiecutter.description }}',
            Code={'ZipFile': build_str},
            Timeout=timeout,
            MemorySize=memory_size,
            Environment={'Variables': {
                'PATH': '/var/task/bin',
                'PYTHONPATH': '/var/task/src:/var/task/lib'
            }}
        )
    except Exception as e:
        print(f'error in creating lambda function')
        raise
    else:
        arn = response['FunctionArn']
        config['function_arn'] = arn

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    exit(0)
else:
    print(f'use existing function ARN {function_arn}')
    exit(0)
    