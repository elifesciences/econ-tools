#!/bin/bash
set -e
source venv/bin/activate

if [ "$#" -ne 1 ]; then
    echo "Usage: ${0} elife-12345"
fi

AWS_DEFAULT_REGION=us-east-1 python econ_article_feeder.py --prefix $1 ct-elife-production-final ct-workflow-starter-queue IngestArticleZip
