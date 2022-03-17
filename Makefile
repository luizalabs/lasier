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
	@poetry run flake8 .
	@poetry run isort . --check
	@poetry run mypy lasier
	@poetry run black --check lasier

test: clean  ## Run unit tests
	@poetry run pytest -x tests/

test-matching:
	@poetry run pytest -rxs --pdb -k$(Q) tests/

coverage:  ## Run unit tests and generate code coverage report
	@poetry run pytest -x --cov lasier/ --cov-report=xml --cov-report=term-missing tests/

install:  ## Install development dependencies
	@poetry install

outdate:  ## Show outdated dependencies
	@poetry show --outdated

release-patch:  ## Create a patch release
	@poetry run bumpversion patch

release-minor:  ## Create a minor release
	@poetry run bumpversion minor

release-major:  ## Create a major release
	@poetry run bumpversion major
