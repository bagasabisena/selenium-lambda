PROJECT_NAME := $(shell python -c "import json;print(json.load(open('config.json'))['project_name'])")
FUNCTION_HANDLER := $(shell python -c "import json;print(json.load(open('config.json'))['function_handler'])")

## remove artifacts like build.zip and chrome driver
clean:
	rm -rf build build.zip
	rm -rf __pycache__
	rm -rf chromedriver.zip headless-chromium.zip

## get selenium chrome driver and chrome headless browser
fetch-dependencies:
	mkdir -p bin/

	# Get chromedriver
	curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
	unzip chromedriver.zip -d bin/

	# Get Headless-chrome
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip headless-chromium.zip -d bin/

	# Clean
	rm headless-chromium.zip chromedriver.zip

## build docker image for testing our selenium locally
docker-build:
	docker image build -t {{ cookiecutter.project_slug }} .

## run selenium locally using docker
docker-run:
	docker container run --rm \
	-e "PYTHONPATH=/var/task/src:/var/task/lib" \
	-e "PATH=/var/task/bin" \
	-v $(shell pwd)/src:/var/task/src \
	-v ${HOME}/.aws/credentials:/root/.aws/credentials:ro \
	$(PROJECT_NAME) src/$(FUNCTION_HANDLER)

## create role if role_arn is empty on config.json
lambda-role:
	@echo create role
	python scripts/create_role.py

## create lambda project if not exists
lambda-create: lambda-role clean
	@echo create lambda function
	# only zip the code for dummy code
	mkdir build
	cp -r src build/.
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	python scripts/create_function.py
	rm -r build/ && rm build.zip

## build zipped package and upload to s3
lambda-build: check-bucket clean
	mkdir build
	cp -r src build/.
	cp -r bin build/.
	# cp -r lib build/.
	pip install -r requirements.txt -t build/lib/.
	sh scripts/slim.sh
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	python -u scripts/cp_s3.py
	rm -rf build
	rm build.zip

## deploy the lambda function
lambda-deploy: lambda-create lambda-build
	python scripts/update_function.py

## check if bucket configuration is set
check-bucket:
	python scripts/check_bucket.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
