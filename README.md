<p align="center"><img src="assets/myna.svg" width="128" alt="Myna"></p>

# Myna

A workbench over [Magpie](https://github.com/agncrow/magpie), written in
Crow: the catalog, queries, notebooks, dashboards, models, a model to ask
and the jobs that run it all, every piece of its state a Magpie log. The
notebooks, the queries, the catalog, the dashboards, the jobs and the
settings are built. The models and the model to ask are not yet, and
their pages say so.

Myna needs Crow 0.8.0 or later and installs Magpie as any dependency.
From this folder:

```
crow install
crow run main.co
```

serves it on port 3800. `crow run -i main.co` interprets it instead, and
starts at once.

## The pages

- **Notebooks** (`/`): a notebook is cells of Crow, run top to bottom as
  one program by the crow on the PATH, in the workspace's folder, so a
  table a cell writes is a log beside the others. Each cell's output,
  status and time are shown under it. A stop or a refusal is shown under
  the cell it names, by the cell's own line, and the cells after it are
  skipped. The side panel names the variables the cells left and the
  tables they read and write. Ctrl+Enter runs, Ctrl+S saves and Escape
  cancels an edit. Every save is a version and every run is kept with its
  output: History lists both, opens a run's output and restores a
  version. A notebook can also run on a schedule.
- **Query** (`/query`): one of Magpie's reading verbs over a table, asked
  as a form: the latest rows (the columns named, or all), a summary
  (grouped by columns, a column reduced by sum, count, mean, min, max,
  std, var, first or last, the rows a predicate admits) or a search of a
  text column (words, phrases, prefixes `kit*`, fuzzy words `kitchn~`).
  The answer is a table and, for a summary, bars. A query is saved by
  name in the workspace's `_queries` log and opened again from the list,
  and Open as notebook writes it as the first cell of a new notebook.
- **Catalog** (`/catalog`): the workspace's tables, each a Magpie log,
  with their columns and their latest rows; Query this table opens the
  query page on it.
- **Dashboards** (`/dashboards`): saved queries side by side as tiles,
  each drawn as bars, a number or a table. A query is added from the
  dashboard or pinned from the Query page; tiles are moved and removed in
  place. Refresh now asks every tile's query again, and a dashboard given
  an interval (1 min, 15 min, 1 h, 1 d) is refreshed by the scheduler.
  Each tile's answer is kept as a Parquet file under `.tiles/`, so a
  dashboard opens without asking its queries.
- **Jobs** (`/jobs`): the scheduler, the schedules and every run.
- **Settings** (`/settings`): the workspace's name, and how long a run may
  take before it is stopped (60 seconds unless set).

The search in the top bar finds notebooks and tables by name.

## The scheduler

A notebook's schedule is kept in the workspace, and the scheduler runs
it. The Jobs page starts the scheduler as a process of its own
(`crow run -i scheduler.co 3800`). Every fifteen seconds it runs the
notebooks that are due and records each run as the schedule's. It ends
when the page asks it to, or when the page has not answered for three
rounds. `crow run scheduler.co` runs it without a page, until the file
`myna_data/_scheduler.stop` is written.

## The workspace

Everything Myna keeps is in `myna_data/` beside the program, each piece a
Magpie log: `_notebooks` (every version of every cell), `_runs` (every
run and its output), `_queries`, `_schedules`, `_settings`, and the tables the
notebooks write. `MYNA_DATA` names another folder. It must lie inside
this checkout, where the programs a notebook runs find `crow_modules/`.

## Tests

```
./test.sh
```

runs every part's blocks, interpreted and then compiled. The tests make
and remove a workspace of their own, `test_data/`, and refuse to run in
`myna_data/`. `./test.sh path/to/crow` tests another crow.

## The code

- `main.co` serves the pages.
- `myna/workspace.co` reads and writes the logs.
- `myna/engine.co` makes a notebook into one program, runs it, and reads
  its output back cell by cell.
- `myna/workbench.co` is the frame every page shares: the sidebar, the
  top bar and the search.
- `myna/queries.co` runs a query, writes it as a cell's Crow and says
  it in a line; the dashboards read saved queries through it, as Ask
  is to.
- `myna/tiles.co` refreshes a dashboard's tiles and says when one is due.
- `myna/query.co`, `myna/notebooks.co`, `myna/catalog.co`,
  `myna/dashboards.co`, `myna/jobs.co` and
  `myna/settings.co` are the pages; `myna/soon.co` holds the pages not
  built yet.
- `scheduler.co` is the scheduler.

The design, the screens and the plan: the architecture document and the
design canvas (private for now). The name: the myna, the clever talking
bird of every Indian town; the mark is Crow's face between two amber
quotation marks, `"(o.o)"`, the one that talks.

## License

Business Source License 1.1: `LICENSE`, in plain words in `LICENSING.md`.
Free for development, testing and non-commercial use, and for commercial
production on one machine per application; hosted services need a
commercial license (vkotinaga@gmail.com). Each version becomes
Apache-2.0 four years after it is published.
