.PHONY: bootstrap deps build test test-fast lint compile reviewer-contract public-benchmark-check secret-scan release-export-check release-check verify docker-build docker-run

PYTHON ?= python3
VENV ?= .venv
PY := $(VENV)/bin/python

bootstrap:
	$(PYTHON) -m venv $(VENV)
	$(MAKE) deps

deps:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e .
	$(PY) -m pip install build ruff

build:
	$(PY) -m build

test:
	$(PY) -m unittest discover -s tests -p "test_*.py" -v

test-fast:
	$(PY) -m unittest discover -s tests -p "test_public_release_export.py" -v
	$(PY) -m unittest discover -s tests -p "test_secret_scan.py" -v

lint:
	$(PY) -m ruff check src tests scripts

compile:
	$(PY) -m compileall -q src scripts tests

reviewer-contract:
	$(PY) scripts/check_reviewer_web_contract.py

public-benchmark-check:
	$(PY) scripts/check_public_benchmark_v11.py

secret-scan:
	$(PY) scripts/secret_scan.py

release-export-check:
	$(PY) scripts/export_public_release.py --check-only

release-check: test-fast reviewer-contract public-benchmark-check secret-scan release-export-check

verify: lint compile test reviewer-contract public-benchmark-check secret-scan release-export-check build

docker-build:
	docker build -f Dockerfile.reproduce -t cogniprint:reproduce .

docker-run:
	docker run --rm cogniprint:reproduce
