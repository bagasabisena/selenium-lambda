# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Requirements

This project uses Python `3.7`. Python 3.7 will also become the runtime for lambda.
This project also depends on `make` and `curl` to run the development command.
`make` and `curl` should be available by default on Mac and Linux machines.

For Windows user, this project has been tested to run on WSL2 Ubuntu.

## Setup the scraper environment

Use python version 3.7 as your python interpreter and install the requirements.

```bash
pip install -r requirements.txt
```

Now we setup the selenium environment. First, we need to download the chrome binary

```bash
make fetch-dependencies
```

then, we create a docker image for running the selenium locally.
We run our handler using Docker,
so our runtime environment during development and production on AWS lambda
is the same.

```bash
make docker-build
```

`docker-build` should only be run once, or anytime your `requirements.txt` changes.

### Configuration

The configuration variable for the project is written on the `config.json` file.

```json
{
    "project_name": The project name. Populated by the template.
    "function_arn": By default this is empty and will be populated by our script. If you have an existing function, you can fill your lambda function ARN here.
    "role_arn": By default this is also empty. The script will create a default role for you. If you have an existing role that you want to use, fill the IAM Role ARN here.
    "function_handler": The entry point of lambda execution. Default to `handler.selenium_handler`.
    "function_timeout": Lambda execution timeout, defaults to 900 (in seconds),
    "function_memory_size": Lambda memory requirements, defaults to 1024 (which should be enough),
    "package_bucket": Since the deployment package is large (~45MB), the package is deployed to S3 instead of pushing it directly to lambda. This set up the S3 bucket for storing the zipped package. No default, but it is required.
    "package_key": The S3 key of the deployed zipped package. Default to 'build.zip'. If you want to put inside folder, prepend those folder, ex: 'folder/subfolder/build.zip'
}
```

## Developing the scraper

All python program should be put inside the `src` folder.
By default, the lambda handler is put inside `src/handler.py` file, under the function `selenium_handler`.
If you change the handler, make sure to change the `"function_handler"` config in `config.json`

You can freely structure your python modules/files, as long as those files are put inside the `src` folder.

### Running/Testing the scraper locally

For running/testing the handler locally, we use docker,
so the runtime between local development and production is similar. The make `docker-run` handles that.

```bash
make docker-run
```

Anytime you change your scraper handler, you can run/test using `make docker-run`.

## Deploying the scraper

First, you must have an S3 bucket ready. The bucket will be used to store the packaged deployment files.
We will not create the bucket for you. Set the bucket name on the `package_bucket` configuration in the `config.json`.

By default, the package file will be stored in the bucket under the key `{{ cookiecutter.project_slug }}/build.zip`. If you want to change that, change the `package_key` configuration in the `config.json`.

Run `make lambda-deploy` to deploy your scraper to AWS lambda.

```bash
make lambda-deploy
```

By default, the command will:

* create a default IAM role for you (`make lambda-role` command)
* create a lambda function for you (`make lambda-create` command)
* package the requirements, slim the python files, zip the package, and upload the zipped package to S3 (`make lambda-build` command)
* update the function code

If you have an existing IAM role, and not wanting the default role created for you, please change the `"role_arn"` config in `config.json` to the IAM role ARN that you want.

The same goes with the lambda function. If you have an existing lambda function that works for you, change the `"function_arn"` to the lambda function ARN that you have.

If both the `role_arn` and `function_arn` are blank in the `config.json` (the default), then a role and function will be created for you.
