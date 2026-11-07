# MLflow's Parts, and How Myna Holds Them

Myna keeps the record of machine-learning work the way MLflow does: the
experiments, the runs inside them, what each run was given and what it
scored, the files it made, the models kept from it, and how a kept model
is called. All of it is written in Crow. Every record is a row of a
Magpie log in the workspace, beside the notebooks' tables. There is no
second database and no Python.

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
