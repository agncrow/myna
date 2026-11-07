# Experiments and Models

Myna keeps the record of machine-learning work the way MLflow does: the
experiments, the runs inside them, what each run was given and what it
scored, the files it made, the models kept from it, and how a kept model
is called. All of it is written in Crow. Every record is a row of a
Magpie log in the workspace, beside the notebooks' tables. There is no
second database and no Python.

This document covers what MLflow's parts are, how Myna holds them, the
pages, the calls a notebook makes, the HTTP API MLflow's own client
talks to, serving and evaluation, how all of it is tested, and what is
not built.

## MLflow's parts, from the start

| Part | The question it answers | What it holds |
|---|---|---|
| Experiment | Which piece of work is this? | A name, an id, tags |
| Run | What happened in one attempt? | Start and end, a status, the user, the source, a parent run |
| Params | What settings did the attempt use? | Key and value, set once |
| Metrics | How well did it do, step by step? | Key, value, step and time; every value kept, so a curve can be drawn |
| Tags | What else is worth saying? | Key and value on runs, experiments, models and versions |
| Datasets | What data was it given? | Name, digest, source, schema, and its use (train, eval) |
| Artifacts | What files did it make? | A folder per run |
| Logged model | Which model came out of the run? | An id, its files, its metrics, the run |
| Registered model | Which model is kept, and which version is live? | A name, numbered versions, aliases (`champion`), stages, tags |
| Prompt | Which prompt text is in use? | Versioned text with `{{variables}}`, kept as a registered model |
| Trace | What did an LLM application do on one request? | A tree of spans with inputs, outputs and times, and feedback |
| Serving | How is the model called? | An HTTP endpoint answering predictions |
| Evaluation | Is the model good enough? | Standard scores, logged to a run |

A notebook logs into a run as it trains. The pages then compare runs,
pick the best, register it, and try it.

## How Myna holds it

A change is a new row. A read takes the latest row per key
(`magpie.latest`). So a delete is a row whose stage is `deleted`, a
restore is another row, history is never rewritten, and two writers never
edit one row in place.

| Log | One row per | Kept |
|---|---|---|
| `_ml_experiments` | experiment change | the latest per id |
| `_ml_runs` | run change | the latest per id |
| `_ml_params` | param | the first per run and key (a param never changes) |
| `_ml_metrics` | metric value logged | every value |
| `_ml_latest` | run and metric | the greatest step, then time, then value |
| `_ml_tags` | tag set or deleted | the latest per entity, id, version and key |
| `_ml_inputs` | dataset given to a run | the latest per run, digest and use |
| `_ml_logged`, `_ml_outputs` | logged model, and the run that made it | the latest |
| `_ml_models`, `_ml_versions`, `_ml_aliases` | registry change | the latest per name, version, alias |
| `_ml_traces` | trace | the latest per trace; spans in the trace's files |

Files live in `.mlartifacts/<experiment>/<run>/artifacts/` and
`.mlartifacts/<experiment>/models/<model id>/artifacts/` in the
workspace, MLflow's own layout, so MLflow's client reads and writes them
in place.

## The pages

The sidebar has **Experiments** and **Models**. Prompts and traces are
tabs inside those two. Every page is drawn with what Myna's other pages
use: the workbench frame, bordered cards, the tab strip from Dashboards,
primary buttons, and a modal for every create or rename.

- **Experiments** (`/experiments`): the experiments on the left, the
  chosen one's runs on the right.
  - The **Runs** tab is a table: name, created, duration, source, status,
    the latest metrics and the params. Child runs sit under their parent
    at any sort. You can filter with MLflow's search grammar
    (`metrics.rmse < 6000 and params.lr = '0.3'`), sort by any column,
    show deleted runs and restore them, pick runs, delete them, compare
    them, or chart them. New and Rename open modals.
  - The **Models** tab lists the logged models.
  - The **Traces** tab lists the traces. Opening one shows its spans as a
    tree, each with a time bar, and the picked span's inputs and outputs.
    Feedback (thumbs up or down) is written on the trace.
  - The **Charts** tab draws one chart per metric across the picked runs,
    with step, time or elapsed time on x.
- **Run** (`/runs/:run_id`): three tabs.
  - **Overview**: status, times, user, source, parent, the description
    (editable), params, latest metrics, tags, datasets and the models it
    logged.
  - **Metrics**: one line chart per metric.
  - **Artifacts**: the folder tree, with a text file opened beside it
    (the first 64 kB).
- **Compare** (`/compare?runs=a,b,c`): params and metrics side by side,
  with ● marking every row whose values differ. There is a scatter of
  any two values (x and y chosen from the lists), and one chart per
  metric with a line per run.
- **Models** (`/models`): the registered models (name, latest version,
  aliases, description), filtered by name, and a Prompts tab. New
  opens a modal.
- **Model** (`/models/:model_name`): the description (editable), the
  versions as a table (version, aliases, stage, source run, created), and
  a version opened in a panel.
  - The panel shows the version's run, its `MLmodel`, and whether it can
    be served. You can set or drop aliases, move the stage, and delete
    the version.
  - Its **Try it** box takes MLflow's input as JSON and shows the
    prediction the served model answers.
  - A prompt's version shows its text with the `{{variables}}`, and a
    form fills them.

The charts are SVG drawn in Crow (`myna/charts.co`). They sort by x, fit
y to the data with 5% room at each end, and leave a gap at a NaN.

## The calls a notebook makes

A notebook cell `use myna.tracking` (and `myna.registry`,
`myna.serving`) and logs with a few calls:

| Call | Does |
|---|---|
| `tracking.start_run[experiment, name]` | Makes the experiment if it is new, starts a run, answers its id |
| `tracking.log_params[run, map]`, `log_param[run, key, value]` | Records settings; a different value for a key already set is refused |
| `tracking.log_metrics[run, map, step]`, `log_metric[run, key, value, step]` | Appends values; NaN and infinities are kept as they are |
| `tracking.log_input[run, frame, name, context]` | Records a dataset: digest, schema and row count, from the frame |
| `tracking.log_text`, `log_table`, `log_artifact` | Writes a file among the run's artifacts |
| `tracking.tag_run[run, key, value]`, `describe_run[run, text]` | Tags; the description is the tag `mlflow.note.content`, as MLflow keeps it |
| `tracking.end_run[run, status]` | `FINISHED`, `FAILED` or `KILLED`, with the end time |
| `tracking.history[run, key]`, `latest_of[run]`, `runs_in[…]` | Reads back, for a later cell |
| `serving.save_model[run, path, code, …]` | Writes a model folder (`MLmodel` and `predict.co`) among the run's artifacts |
| `registry.register[run, path, name]` | Makes the model if it is new and adds a version from the run's folder |
| `registry.set_alias[name, alias, version]`, `transition[…]` | Aliases and stages |
| `serving.evaluate[name, ref, rows, truth, kind, run]` | Scores a version on rows against the truth, logging each score to the run |
| `serving.score[name, ref, body]` | Asks a version for predictions, as the HTTP endpoint does |

`tests/mlflow/house_prices.co` uses every one of them on sample data.

## MLflow's HTTP API

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

## Serving and evaluation

A model is a folder of files. Its `MLmodel` file, in MLflow's format,
names the flavor `crow` and the input and output columns. Beside it,
`predict.co` holds `fn predict[rows]`, which answers one prediction per
row, plus whatever files the model reads (its weights).

**Serving.** `POST /serve/:model/:ref/invocations` takes a version
number, an alias or `@alias` as `:ref`. The body may be any of MLflow's
input forms: `dataframe_split`, `dataframe_records`, `instances` or
`inputs`. The answer is `{"predictions": […]}`.

The model runs by the crow on the PATH, interpreted, in a scratch copy
of its folder (`.serving/<id>`) and under a time limit. So a slow or
failing model cannot stop the workbench, and a model cannot write into
its own folder. Bad input gets a 400 with the reason.

**Evaluation.** `serving.evaluate` asks the model about the rows and
scores what it answers against the truth, with scikit-learn's
definitions:

- For a regressor: mean squared error, root mean squared error, mean
  absolute error, R² (1 for a perfect fit when the truth does not vary,
  0 otherwise), max error, and mean absolute percentage error.
- For a binary classifier, with 1 as the positive class: accuracy,
  precision, recall and F1, each 0 where its denominator is 0.

Each score is logged as a metric on the run named.

## MLflow's known bugs, and how Myna avoids them

MLflow's issue tracker was read for bugs in the parts Myna rebuilds, and
the ones that apply are held off by design:

- **Zero is a value.** A step or a time of 0 is kept, not read as
  missing.
- **NaN.** NaN is stored and shown as NaN. It fails every comparison and
  sorts last.
- **History.** The history of a key never logged is an empty list, in
  step-then-time order.
- **The latest metric** is the one at the greatest step, not the last
  row written.
- **Search is parsed, never pasted into a query.**
  - Numbers compare as numbers.
  - Operators may be in any case, either quote mark may be used, and
    backticked keys are read.
  - Paging has one stable order with the id last, so no run is seen
    twice or skipped.
  - A bad page token or `IS NULL` is refused with
    `INVALID_PARAMETER_VALUE`.
- **Names.** An experiment's name, deleted or not, stays taken. Default
  (id 0) is made once.
- **Renames.**
  - A run's rename changes its name and its `mlflow.runName` tag only.
  - A registered model's rename moves its tags, aliases and versions.
- **Deleted versions.** Deleting a version removes its aliases.
- **Stages.** `archive_existing_versions` archives every other version
  in the stage.
- **Files.**
  - A path with `..`, an absolute path or a backslash is refused.
  - A version's source must lie among its run's files.
  - A missing file answers with the relative path, never the server's.
- **Prompts.** A prompt is formatted in one pass, so a value's text is
  never formatted again.
- **Charts** are sorted by x with y fitted to the data, and children
  stay under their parent at any sort.

## Tests

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

## Not built

Everything is built in Crow, with no integration with an outside
framework. These parts of MLflow are left out for that reason:

| MLflow feature | Why not | What Myna has |
|---|---|---|
| Python flavors (scikit-learn, PyTorch, TensorFlow, XGBoost, transformers, …) and serving them | Each is a Python framework | The `crow` flavor; MLflow's client can still store any model's files as artifacts |
| Autologging | It patches Python libraries | Explicit `log_*` calls |
| Cloud artifact stores (S3, Azure, GCS, HDFS) | Outside services | The workspace folder |
| SQL tracking backends | Magpie is the store | Magpie logs |
| Databricks, Unity Catalog, the permissions plugin | Outside platform | Myna's workspace |
| AI Gateway, deployments to SageMaker, Azure ML, Ray | Outside services | Myna's own serving |
| Docker images, conda and virtualenv environments | Python packaging | A model folder run by crow |
| GenAI judges (`mlflow.genai` scorers) | They call outside models | Evaluation's scores, and feedback on traces |
| OpenTelemetry trace export and import (`/v1/traces`, protobuf) | Outside protocol | Traces kept in Myna, spans as JSON |
| Signature inference from Python types | Python | The columns written in `MLmodel` |
| Recipes | Retired in MLflow | Notebooks and jobs |

And these are not built yet, though they are Crow work:

- **The artifact proxy** (`/api/2.0/mlflow-artifacts/…` upload and
  download). MLflow's client writes and reads the workspace's files
  directly, which works when it runs on the same machine. A client
  elsewhere needs the proxy.
- **Projects** (`MLproject` entry points run as jobs).
- **Classifier extras:** log loss, the confusion matrix, and a table of
  every scored row (`eval_results`).
- **On the pages:**
  - previews of images and tables among the artifacts;
  - a value shown on hover over a chart;
  - a diff between two prompt versions;
  - downloading a file.
- **Serving speed.** A served model is started for each request rather
  than kept warm: about a second for each call.
- **A logged-model record for a saved model.** `serving.save_model`
  writes the model's files among the run's artifacts, and a run's page
  lists them under Artifacts. It makes no logged-model record, as MLflow
  3's `log_model` does, so the run's Logged models card stays empty.
  MLflow's client's own `log_model` does make one.

Interpreted (`crow run -i main.co`), the Experiments pages answer a click
in 9 to 17 seconds once a few sessions are open. Each refresh derives
every open page again from the logs. Compiled (`crow run main.co`, the
default), the same click answers in under 0.1 seconds.
