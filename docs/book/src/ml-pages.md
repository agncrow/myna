# The Experiments and Models Pages

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
