# Logging from a Notebook

A cell like this one makes a run, records what it was given and how it
did, and ends it. The run then shows on the Experiments page:

```crow,ignore
use myna.tracking

tracking.ready[]
run = tracking.start_run['house-prices', 'linear-lr0.1']
p = tracking.log_params[run, map[lr = '0.1', epochs = '60']]
for step in range[60]
    m = tracking.log_metric[run, 'rmse', 1000.0 / (step + 1), step]
done = tracking.end_run[run, 'FINISHED']
```

Each call answers what it wrote, or why not, and a cell keeps the
answer in a name. A value that can fail may not be dropped in Crow, so a
failed write stops the cell rather than passing unseen.


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
