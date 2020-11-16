# {{ cookiecutter.project_name }} Selenium Scraper

## Developing the scraper

Install the python requirements. Make sure to use python version 3.7

```bash
conda create -n {{ cookiecutter.project_name}} python=3.7
pip install -r requirements.txt
```

Now we setup the environment. First, we need to download the chrome binary

```bash
make fetch-dependencies
```

then, we create the docker image.

We run our handler using Docker,
so our runtime environment during development and production on AWS lambda
is the same.

```bash
make docker-build
```

Next is to populate the `.env` file that contains configs for our app.
Copy the .env.sample for the template

For running/testing the handler

```bash
make docker-run
```

## Deploying the scraper

First we need to create the AWS lambda project.
A make command will handle that

```bash
make lambda-create
```

Copy the ARN and put in the `.env` file

Then we need to package the `.zip` file and upload the zipped file
to an S3 bucket as indicated by `PACKAGE_BUCKET` and `PACKAGE_KEY` config.

```bash
make lambda-build
```

Afterwards, a simple Make command will handle the deployment

```bash
make lambda-deploy
```
