#!/bin/bash
set -e # everything must succeed.
if [ ! -d venv/bin/python3 ]; then
    rm -rf venv
    python3 -m venv venv
fi
source venv/bin/activate
pip install pip wheel --upgrade
pip install -r requirements.txt
