#!/bin/bash
set -e
source venv/bin/activate

if [ "$#" -ne 1 ]; then
    echo "Usage: ${0} elife-12345-vor-r1"
fi

PYTHONPATH=. AWS_DEFAULT_REGION=us-east-1 python econtools/econ_article_feeder.py --prefix $1 -r 1 ct-elife-production-final ct-workflow-starter-queue InitialArticleZip
