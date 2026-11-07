# MLflow's HTTP API

Myna answers MLflow's own protocol, so `mlflow.set_tracking_uri(
'http://localhost:3800')` and MLflow's Python client work against it.
The client is the test, not an integration Myna depends on.

| Area | Endpoints |
|---|---|
| Experiments (`/api/2.0/mlflow/experiments/…`) | create, get, get-by-name, search, update, delete, restore, set-experiment-tag, delete-experiment-tag |
| Runs (`/api/2.0/mlflow/runs/…`) | create, get, update, delete, restore, search, log-metric, log-parameter, log-batch, set-tag, delete-tag, log-inputs, outputs; `metrics/get-history`; `artifacts/list` |
| Logged models (`/api/2.0/mlflow/logged-models…`) | create, get, finalize, delete, search, set and delete tags |
| Registered models (`/api/2.0/mlflow/registered-models/…`) | create, get, rename, update, delete, search, alias (set, delete, get by alias), set-tag, delete-tag, get-latest-versions |
| Model versions (`/api/2.0/mlflow/model-versions/…`) | create, get, update, delete, search, get-download-uri, set-tag, delete-tag, transition-stage |
| Traces (`/api/3.0/mlflow/traces…`) | start, get, batchGet, search, tags, delete, assessments (create, get, delete) |

Errors take MLflow's form: `{"error_code": "RESOURCE_DOES_NOT_EXIST",
"message": …}` with status 404, `RESOURCE_ALREADY_EXISTS` and
`INVALID_PARAMETER_VALUE` with 400.
