PIP=pip
PYTHON=python3

all: help

help:
	@echo "install ------------ - Install requirements."
	@echo "test --------------- - Run unittests using current python."
	@echo "dist --------------- - Rebuild."
	@echo "  clean ------------ - Clean all distribution build artifacts."
	@echo "    clean-pyc ------ - Remove .pyc/__pycache__ files."
	@echo "    clean-build ---- - Remove setup artifacts."
	@echo "  build ------------ - Rebuild python package."

	@echo "upload ------------- - Upload built python package on pypi server."

install:
	$(PIP) install -r requirements/dev.txt
	$(PIP) install -r requirements/requirements.txt
	$(PYTHON) -m pip install --upgrade build twine

test:
	$(PYTHON) -m pytest

clean-pyc:
	-find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	-find . -type d -name "__pycache__" | xargs rm -r

clean-build:
	rm -rf build/ dist/ .eggs/ *.egg-info/

clean: clean-pyc clean-build

build:
	$(PYTHON) -m build

dist: clean build

upload:
	$(PYTHON) -m twine upload -r "${PYPISERVERNAME}" dist/*
