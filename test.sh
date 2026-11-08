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
parts="myna/workspace.co myna/engine.co myna/queries.co myna/query.co myna/tiles.co myna/projects.co myna/access.co myna/dashboards.co myna/project.co myna/users.co myna/grants.co myna/code.co myna/catalog.co myna/jobs.co myna/settings.co myna/tracking.co myna/search.co myna/registry.co myna/traces.co myna/mlapi.co myna/charts.co myna/experiments.co myna/runs.co myna/serving.co myna/models.co myna/drawn.co"
for part in $parts; do
    echo "== $part"
    "$crow" test "$part"
done
for part in myna/query.co myna/dashboards.co myna/project.co myna/users.co myna/grants.co myna/code.co myna/catalog.co myna/jobs.co myna/settings.co myna/mlapi.co myna/experiments.co myna/runs.co myna/models.co; do
    echo "== $part, compiled"
    "$crow" test --compiled "$part"
done
rm -rf test_data
# the workbench drawn by Lory (drawn/main.co): its own tests, run where Lory
# is installed beside it (crow install in drawn/)
if [ -e drawn/crow_modules/lory ]; then
    echo "== drawn/main.co"
    (cd drawn && "$crow" test main.co)
else
    echo "== drawn/main.co skipped: Lory is not installed (crow install in drawn/)"
fi
# a model trained, tracked, registered, evaluated and served, every number
# held to the same model trained in Python (needs scikit-learn: the venv
# MLflow's client check uses, ~/.venvs/mlflow, or MYNA_PYTHON)
python="${MYNA_PYTHON:-$HOME/.venvs/mlflow/bin/python}"
if [ -x "$python" ]; then
    echo "== tests/mlflow/house_prices.co, held to Python"
    "$python" tests/mlflow/house_prices.py "$crow"
    "$python" tests/mlflow/house_prices.py "$crow" --compiled
else
    echo "== tests/mlflow/house_prices.py skipped: no Python with scikit-learn at $python"
fi
echo "every test passed"
