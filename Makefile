# Makefile

.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

PACKAGE = clustercron

.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: clean
clean: clean-build clean-pyc clean-test clean-docs ## Remove all build, test, coverage, docs and Python artifacts

.PHONY: clean-build
clean-build: ## Remove build artifacts.
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

.PHONY: clean-test
clean-test: ## Remove test and coverage artifacts.
	rm -f .coverage
	rm -f coverage.xml
	rm -rf .pytest_cache
	rm -rf .tox/
	rm -f .coverage
	rm -rf htmlcov/

.PHONY: clean-docs
clean-docs: ## Remove files in docs/_build
	$(MAKE) -C docs clean

.PHONY: lint
lint: ## Run all pre-commit hooks on all files
	pre-commit run --all-files --show-diff-on-failure

.PHONY: test
test: ## Run tests quickly with the default Python.
	pytest --cov=$(PACKAGE)

.PHONY: tox
tox: ## Run tests on every Python version with tox.
	tox

.PHONY: coverage
coverage: ## Check code coverage quickly with the default Python.
	coverage erase
	coverage run --source $(PACKAGE) -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: docs
docs: clean-docs ## Generate Sphinx HTML documentation, including API docs.
	rm -f docs/$(PACKAGE).rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/$(PACKAGE)
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

.PHONY: release
release: clean tox build ## Package and upload a release.
	twine upload dist/*

.PHONY: build
build: clean-build ## Builds source and wheel package.
	python -m build
	python -m twine check --strict dist/*

.PHONY: devenv
devenv: ## Install package development mode + dependencies.
	pip install -U pip wheel setuptools
	pip install -e ".[dev]"
