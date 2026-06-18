.PHONY: bootstrap test public-benchmark-check secret-scan release-check

PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

bootstrap:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .

test:
	$(PY) -m unittest tests/test_public_release_export.py -v

public-benchmark-check:
	$(PY) scripts/check_public_benchmark_v11.py

secret-scan:
	$(PY) scripts/secret_scan.py

release-check: test public-benchmark-check secret-scan
