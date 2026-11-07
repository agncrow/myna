# Myna

Myna is a workbench for data and machine learning, written in Crow over
[Magpie](https://agncrow.github.io/magpie/). It holds everything a team
does with data in one place:

- the catalog of tables;
- queries, asked as forms, and dashboards made of them;
- notebooks of Crow cells;
- experiments and models, as MLflow keeps them;
- the jobs that run all of it on a schedule.

Every piece of its state is a Magpie log in one folder, the workspace.
The notebooks' tables sit beside Myna's own records. There is no second
database, no Python and no JavaScript framework: the pages are Crow
views, served by Crow, in both of its modes.

## What it is made of

| Part | Written in | Kept in |
|---|---|---|
| The pages | Crow views (`use ui`) | nothing: they are derived from the logs |
| Notebooks and their runs | Crow, run by the crow on the PATH | `_notebooks`, `_runs` |
| Queries and dashboards | Magpie's reading verbs | `_queries`, `_dashboards`, `_tiles` |
| Experiments and models | Crow, answering MLflow's own client | `_ml_*` logs and `.mlartifacts/` |
| The scheduler | a Crow program of its own | `_schedules`, `_runs` |

## Reading this book

Part I walks through the workbench, one page at a time. Part II is
experiments and models: what MLflow's parts are, how Myna holds them,
and how a notebook, the pages and MLflow's own client reach them. Part
III is the reference: tests, the code, and what is not built.

## The name

The myna is the clever talking bird of every Indian town. The mark is
Crow's face between two amber quotation marks, `"(o.o)"`: the one that
talks.

## Status

Every page but the model to ask is built, and that page says so. Myna's
source is at [github.com/agncrow/myna](https://github.com/agncrow/myna),
under the Business Source License 1.1 ([Licensing](licensing.md)).
