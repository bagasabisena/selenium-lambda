# Cookiecutter Template for Selenium Python on AWS Lambda

Use this [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) template to generate a selenium python project
that can be run on AWS Lambda.

Why AWS Lambda? You get a selenium crawler that costs you money on runtime only.
This selenium scraper includes a chrome headless browser and chrome driver.

This project is heavily inspired by this great [blog](https://robertorocha.info/setting-up-a-selenium-web-scraper-on-aws-lambda-with-python/)

## Usage

First, install cookiecutter package.

```bash
pip install cookiecutter
```

Then, run against this repo.

```bash
cookiecutter https://github.com/bagasabisena/selenium-lambda
```

or you can clone the repo first and run the template locally

```bash
git clone https://github.com/bagasabisena/selenium-lambda
cookiecutter selenium-lambda/
```

Answer the prompt, and your project is now ready!

Go to the project, and check the `README.md`
for further instruction.

## Todos

* [ ] create a Make command for invoking lambda
* [ ] include a minimal IAM JSON policy in the README.md
* [ ] Check for newer chrome driver and headless chromium
* [ ] migrate to serverless framework?
