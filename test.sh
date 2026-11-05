#!/bin/bash
# Myna's tests: every part's blocks, interpreted and then compiled.
#
#   ./test.sh [crow]
#
# The tests make and remove a workspace of their own, test_data/ (MYNA_DATA),
# and refuse to run in myna_data/, the workspace people work in. It lies
# inside the checkout so that the programs a notebook runs find the packages
# in crow_modules/.
set -euo pipefail
crow="${1:-crow}"
cd "$(dirname "$0")"
export MYNA_DATA=test_data
parts="myna/workspace.co myna/engine.co myna/notebooks.co myna/catalog.co myna/jobs.co myna/settings.co"
for part in $parts; do
    echo "== $part"
    "$crow" test "$part"
done
for part in myna/notebooks.co myna/catalog.co myna/jobs.co myna/settings.co; do
    echo "== $part, compiled"
    "$crow" test --compiled "$part"
done
rm -rf test_data
echo "every test passed"
