<p align="center"><img src="assets/myna.svg" width="128" alt="Myna"></p>

# Myna

A workbench over [Magpie](https://github.com/agncrow/magpie), written in
Crow: the catalog, queries, notebooks, dashboards, experiments and
models, a model to ask and the jobs that run it all, every piece of its
state a Magpie log. Everything but the model to ask is built, and its
page says so. Experiments and Models do what MLflow does, and answer
MLflow's own client.

**The article and the Myna Book:** <https://agncrow.github.io/myna/>
(the book's chapters are `docs/book/src`, rendered by
`docs/book/site.co`; `.github/workflows/pages.yml` publishes both on
every push to main that touches them).

Myna needs Crow 0.8.2 or later
(`curl -fsSL https://raw.githubusercontent.com/agncrow/crow/main/install.sh | bash`). Myna installs Magpie as any dependency:

```
git clone https://github.com/agncrow/myna
cd myna
crow install
crow run main.co
```

serves it on port 3800. `crow run -i main.co` interprets it instead, with
no build, though it takes about two minutes to read the program before
it serves.

What Lory draws in WebGL — the Code page's editor (`drawn/edit.co`) and
the drawn workbench (`drawn/main.co`) — is built for the web once, where
Lory is installed beside it:

```
cd drawn
crow install                       # lory, from ../../lory/packages/lory
crow build --target web edit.co    # the editor → edit_web/, served at /edit/
crow build --target web main.co    # the workbench → main_web/, served at /drawn/
```

`myna/web/` links both builds, and the server answers their files.
Without the editor's build, the Code page's cells say the editor did not
load.

## Myna as a package

An app built on Myna — finchdash is one — depends on the package folder
`myna/` (the modules, the styles, the widgets, the web builds' links) and
serves Myna's pages beside its own, from its own folder, which is the
open project:

```
name = 'finchdash'
deps = map[magpie = 'github.com/agncrow/magpie/packages/magpie@v0.1.1', myna = '../myna/myna']
```

```
use web, ui
use myna
use app.scanner
here = myna.ready[3900]
serve[3900, wide = true, refresh = 10, files = myna.builds[]]
pages = myna.pages[]
page['/scanner', scanner.render]
```

`myna.ready` opens the app's folder as the project, readies the
workspace (`myna_data/` beside the app), links Myna's `css/` and
`widgets/` where the app has none of its own, and notes the port for the
scheduler; `myna.pages` registers every page and route of the workbench.
A dashboard of the manifest that names a page (`"page": "/scanner"`) is
listed in the sidebar, and its tab on the Dashboards page opens the page.
The design is in `docs/platform.md`.

## The pages

- **Projects** (`/projects`): open a Crow project's folder by its whole
  path, and Myna works in that project until you close it. A project is
  a folder with a `crowfile` and a manifest, `myna.json`, which names
  its data folder, the programs it compiles, its dashboards, its
  schedules and its settings; its notebooks are `notebooks/*.co` and its
  saved queries `queries/*.json`. Code is files in the project, data is
  logs in its data folder (`docs/platform.md`, The rule). The page lists
  each program with whether it is compiled. Compile builds every program
  into the project's `bin/` in the background and stamps each binary with
  a fingerprint of the sources, so a dashboard runs the binary while it
  is fresh. New project makes a folder with a Hello
  dashboard whose program writes a table, and `git init`. While no
  project is open, Myna works in its scratch project, `myna_data/scratch`.
  The format is set out in finchdash's `docs/project-format.md`, and
  where projects are going — workspaces with users and access, projects
  as apps built on Myna as a package, the workspace server — in
  `docs/platform.md`.
- **Code** (`/`): the project's files in a tree, the notebooks first,
  each opened in place as a tab. A `.co` file is shown as cells — a
  notebook is a Crow program, `notebooks/<name>.co`, whose cells are
  marked by `--- %%` lines, and a file without marks is one cell — or as
  text; any other file (the manifest, styles, a note) as text. Cells run
  top to bottom as one program by the crow on the PATH, in the data
  folder, so a table a cell writes is a log beside the others; each
  cell's output, status and time are shown under it, a stop or a refusal
  under the cell it names, and the cells after it are skipped. More runs,
  tests or type-checks the file whole, its output in the console under
  the editor, and sets a schedule (kept in the manifest). The side panel
  names the variables the cells left and the tables they read and write.
  The cell or file being edited is drawn by Lory's editor in WebGL
  (`drawn/edit.co`, mounted by `widgets/editor.js`): line numbers, Crow
  coloured, Tab and Shift+Tab, Enter keeping the indent, the wheel
  scrolling by the pixel, a paste as typed text. Ctrl+Enter saves and
  runs, Ctrl+Shift+Enter runs every cell, Ctrl+S saves and Escape
  cancels an edit. Every save
  writes the file; every run is kept with its output. History lists the
  runs and the file's commits and restores one; the Git drawer shows the
  branch and the changes, makes a repository, commits, pulls and pushes.
- **Query** (`/query`): one of Magpie's reading verbs over a table, asked
  as a form: the latest rows (the columns named, or all), a summary
  (grouped by columns, a column reduced by sum, count, mean, min, max,
  std, var, first or last, the rows a predicate admits), a search of a
  text column (words, phrases, prefixes `kit*`, fuzzy words `kitchn~`),
  or the newest run: the rows a program's newest run wrote to a table
  that marks each row with its `run`.
  The answer is a table and, for a summary, bars. A query is saved by
  name as a file, `queries/<name>.json`, and opened again from the list,
  and Open as notebook writes it as the first cell of a new notebook.
- **Catalog** (`/catalog`): the workspace's tables, each a Magpie log,
  with their columns, their latest rows and who writes them (Myna, the
  open project or the notebooks); Query this table opens the query page
  on it.
- **Dashboards** (`/dashboards`): queries side by side as tiles, each
  drawn as bars, a number or a table. A dashboard is the manifest's
  (`myna.json`, `dashboards`): a tile is added from a saved query, here
  or pinned from the Query page, and holds its query inline; tiles are
  moved and removed in place, and every change is written to the
  manifest. Refresh now asks every tile's query again, and a dashboard
  given an interval (1 min, 15 min, 1 h, 1 d) is refreshed by the
  scheduler. Each tile's answer is kept as a Parquet file under
  `data/.tiles/`, so a dashboard opens without asking its queries. A
  dashboard can name a program. Run runs that program with the
  dashboard's parameters (`name=value` lines, kept in the manifest's
  settings), then refreshes the tiles. It runs the binary in `bin/` when
  one was built from the sources as they are now, and interprets the
  program otherwise. Each run's output is kept with it on the Jobs page.
- **Experiments** (`/experiments`): MLflow's tracking. Each experiment's
  runs are shown with their params and metrics, searched in MLflow's
  grammar, sorted, compared and charted. Logged models and traces have
  tabs of their own. A run's page (`/runs/:id`) shows its overview, its
  metric curves and its files, and Compare (`/compare`) sets runs side
  by side.
- **Models** (`/models`): the registry. A model's versions have
  aliases, stages and tags, and a version can be tried on the page and
  served at `/serve/:model/:ref/invocations`. Prompts have their own
  tab. All of it is in the book's Part II (`docs/book/src`).
- **Jobs** (`/jobs`): the scheduler, the schedules and every run.
- **Users** (`/users`) and **Access** (`/access`), an admin's pages: who
  may sign in, with a role (an admin does everything; a member what their
  grants allow), and each project's grants (viewer, editor, owner). A
  workspace with no users is one person's own: no page asks for a
  sign-in. Adding the first user, an admin, signs you in as them, and
  from then on every page asks for a sign-in; a reader with no grant on
  the open project is told so, and a reader without an editor's grant
  changes nothing. The design, and what comes next: `docs/platform.md`.
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

## Myna's folder

Myna's own folder is `myna_data/` beside the program (`MYNA_DATA` names
another; it must lie inside this checkout, where the scratch project's
programs find `crow_modules/`). It holds the workspace's records, each a
Magpie log — `_projects`, `_users`, `_grants` — and the scratch project,
`scratch/`: a project like any other (`crowfile`, `myna.json`,
`notebooks/`, `queries/`, `data/`) worked in while none is open. A
project's data folder holds `_runs` (every run and its output),
`_answers` (each tile's last refresh), the experiments and models, and
the tables its programs and notebooks write.

## Tests

```
./test.sh
```

runs every part's blocks, interpreted and then compiled. It then holds a
model trained, served and evaluated in Myna to the same model trained in
Python (`tests/mlflow/house_prices.py`, which needs scikit-learn). The
tests make and remove a workspace of their own, `test_data/`, and refuse
to run in `myna_data/`. `./test.sh path/to/crow` tests another crow.
`tests/mlflow/client_check.py` drives MLflow's own Python client against
a running Myna.

## The code

- `main.co` serves the pages.
- `myna/workspace.co` reads and writes the logs.
- `myna/engine.co` makes a notebook into one program, runs it, and reads
  its output back cell by cell.
- `myna/workbench.co` is the frame every page shares: the sidebar, the
  top bar and the search.
- `myna/access.co` is who may do what: the users and their roles, the
  grants, the sign-in, and the derivations every page reads (the
  reader, and whether they may read, write or grant); `myna/users.co`
  and `myna/grants.co` are their pages.
- `myna/queries.co` runs a query, writes it as a cell's Crow and says
  it in a line; the dashboards read saved queries through it, as Ask
  is to.
- `myna/tiles.co` refreshes a dashboard's tiles and says when one is due.
- `myna/tracking.co`, `myna/registry.co`, `myna/search.co`,
  `myna/traces.co` and `myna/serving.co` are the experiments and
  models: the store, the registry, MLflow's search grammar, traces, and
  serving and evaluation. `myna/mlapi.co` answers MLflow's HTTP API over
  them, and `myna/charts.co` draws their charts.
- `myna/experiments.co`, `myna/runs.co` and `myna/models.co` are their
  pages.
- `myna/query.co`, `myna/code.co`, `myna/catalog.co`,
  `myna/dashboards.co`, `myna/jobs.co` and
  `myna/settings.co` are the pages; `myna/soon.co` holds the pages not
  built yet.
- `scheduler.co` is the scheduler.
- `docs/book/` is the Myna Book and `site/` the article;
  `.github/workflows/pages.yml` publishes them.

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
