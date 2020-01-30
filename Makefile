.PHONY: help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Clean cache and temporary files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -rf *.egg-info
	@rm -f .coverage

check:  ## Run static code checks
	@flake8 .
	@isort --check

test: clean  ## Run unit tests
	@py.test -x tests/

coverage:  ## Run unit tests and generate code coverage report
	@py.test -x --cov lasier/ --cov-report=xml --cov-report=term-missing tests/

install:  ## Install development dependencies
	@pip install -r requirements-dev.txt

outdate:  ## Show outdated dependencies
	@pip list --outdated --format=columns

release-patch:  ## Create a patch release
	@bumpversion patch

release-minor:  ## Create a minor release
	@bumpversion minor

release-major:  ## Create a major release
	@bumpversion major
