# How Experiments and Models Are Tested

`./test.sh` runs every part's test blocks, interpreted and then compiled
for the pages. The parts are tracking, search, registry, traces, mlapi,
charts, experiments, runs, serving and models. It then runs two checks
against Python:

- **`tests/mlflow/house_prices.co`** makes 200 houses (area, rooms and
  age, giving a price with a fixed noise), holding every fifth one out.
  - It fits a linear model by gradient descent at three learning rates,
    one run each, logging the error at every epoch.
  - It saves each run's model with its weights written into
    `predict.co`.
  - It registers the best run as `house-price` with the alias
    `champion`, evaluates it on the held-out rows, and asks the served
    model for three predictions.
- **`tests/mlflow/house_prices.py`** trains the same model in plain
  Python loops, adding in the same order. It checks every number the
  Crow run prints:
  - the centres and spreads, every run's weights and final error, and
    the three served predictions, all exactly;
  - scikit-learn's six scores to 1e-12, since numpy adds in another
    order.

  It runs once interpreted and once compiled. It needs Python with
  scikit-learn (`~/.venvs/mlflow`, or `MYNA_PYTHON`).

`tests/mlflow/client_check.py` drives MLflow's own Python client
(`pip install mlflow`) against a running Myna through 25 checks:

- experiments, runs, params and metric history, tags and search;
- artifacts, and a scikit-learn model logged as files;
- the registry with versions, aliases, stages and tags;
- deletes and restores.

Run Myna on a scratch `MYNA_DATA` first.
