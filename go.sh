#!/bin/sh

export PIP_QUIET=1
if [ ! -d ".venv" ]
then
    echo "Creating a python virtual environment..."
    python -m venv .venv
    unset PIP_QUIET # Use more verbose pip install output the first time.
fi

source .venv/bin/activate
pip install --requirement requirements/prod.txt
exec python -m walkingpadfitbit.main $*
