#!/bin/bash
set -e

source venv/bin/activate
PYTHONPATH=. AWS_DEFAULT_REGION=us-east-1 python econtools/econ_article_feeder.py -p $1 -r 1 elife-production-final workflow-starter-queue SilentCorrectionsIngest
