#!/bin/bash
set -e # everything must succeed.
if [ ! -d venv/bin/python3 ]; then
    rm -rf venv
    virtualenv --python=`which python3` venv
fi
source venv/bin/activate
pip install -r requirements.txt
