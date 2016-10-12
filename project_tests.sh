#!/bin/bash
set -e

rm -rf venv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pytest test_feeder.py
