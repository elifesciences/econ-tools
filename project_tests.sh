#!/bin/bash
set -e

rm -rf venv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pylint -E *.py
coverage run -m pytest econtools/test_feeder.py
coverage report -m econtools/*.py

