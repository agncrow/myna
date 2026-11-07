# Serving and Evaluation

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
