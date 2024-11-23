#!/bin/sh

platform=$(python -c "import sys; print(sys.platform)")
pip-compile requirements/dev.in --output-file requirements/lock/$platform/dev.txt
pip-compile requirements/prod.in --output-file requirements/lock/$platform/prod.txt
git diff -u --ignore-all-space requirements/lock/$platform > diff-lock-$platform.patch
