# The Workspace and Settings

## The workspace

Everything Myna keeps is in one folder, `myna_data/` unless `MYNA_DATA`
names another, and each piece is a Magpie log:

| Log | Holds |
|---|---|
| `_notebooks` | every version of every cell |
| `_runs` | every run and its output |
| `_queries` | saved queries |
| `_dashboards`, `_tiles` | dashboards and their tiles |
| `_schedules` | the notebooks' schedules |
| `_settings` | the workspace's settings |
| `_ml_*` | experiments and models ([how](mlflow.md)) |
| any other name | a table a notebook wrote |

A change is a new row, and a read takes the latest row per key. So
nothing is edited in place, and the history of every record is kept.

## Settings

The Settings page (`/settings`) holds the workspace's name, and how long
a run may take before it is stopped (60 seconds unless set).

## Search

The search in the top bar finds notebooks and tables by name.
