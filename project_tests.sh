#!/bin/bash
set -e

rm -rf venv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
coverage run -m pytest test_feeder.py
coverage report -m econ_article_feeder.py

