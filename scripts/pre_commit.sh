#!/bin/bash

CHANGED_PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep ".py\$")

make clean-UFO

if [ -z "$CHANGED_PYTHON_FILES" ]
then
   echo "No Python files found. No reason to run checks."
   exit 0
fi

set -e

echo "list of new/changed/deleted files: $CHANGED_PYTHON_FILES"

make check

echo "All checks successfully passed."

# add this script to .git/hooks/pre-commit
# chmod a+x .git/hooks/pre-commit
