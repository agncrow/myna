# Myna as a platform: workspaces, projects, dashboards and apps

Written 2026-11-07, while finch's pages were being rebuilt as a project
on Myna, and settled with its owner in three rounds. It sets out the
design so the later parts (users and access, the workspace server) are
built on the same terms as what is built now. The parts not built yet
are marked so.

## The rule

**Code is files in a repository; data is logs in Magpie.** Magpie is a
data store, not a place for development: no notebook, query, dashboard,
schedule or setting is kept as rows. They are files, and git keeps their
history. What the system produces — tables, a run's output and status,
an experiment's metrics, a model's artifacts, a tile's cached answer —
is data, and is kept in the project's data folder as logs and files.

## The three words

**Workspace.** The unit of people and access. A workspace holds users,
their roles and what each may see and do (not built yet), and its
projects. One Myna server is one workspace; a company with several teams
runs several. Its own records are logs under `myna_data/`: `_projects`
(the projects it knows) now; `_users`, `_members`, `_grants` when access
is built. These are records about people and folders, not code.

**Project.** A git repository and its data folder. Every project is a
repository, an exploration included: someone exploring data gets a
project of their own, so it can be granted, backed up and retired on its
own. The repository is a Crow project: a `crowfile` naming its
dependencies, the manifest `myna.json`, its notebooks, queries and
dashboards as files, and — for an app — its pages, modules and programs.
The data folder (`data/` unless the manifest or the workspace says
otherwise) holds the logs its programs and notebooks write, copied data,
runs, experiments, models and tile caches. It is not committed. A
project may name several data folders (paper and production, say; not
built yet).

```
project/
  crowfile          deps: magpie; myna, lory, kite for an app
  myna.json         name, data folders, dashboards, jobs' schedules, settings
  notebooks/        each a .co program with cell marks (below)
  queries/          each a saved query, one JSON file
  app/              an app's pages (scanner.co, …)        — app projects
  finch/            its modules                            — app projects
  jobs/             its programs (import.co, parity.co)    — app projects
  main.co           use myna; Myna's pages and the app's   — app projects
  css/app.css       the app's look                         — app projects
  data/             the logs and artifacts (not committed)
```

One shape for every project: an exploration is the first six lines; an
app adds the rest. New project makes the folder, runs `crow install` and
`git init`, and ignores `data/`, `bin/` and the build's caches.

**Dashboard.** A page of a project that shows its data and acts on it:
inputs, buttons and tables, not only charts. Two kinds, one list under
Dashboards in the project's sidebar:

| Kind | Made where | Kept as | For |
|---|---|---|---|
| Tile dashboard | Myna's own pages, from saved queries | an entry in `myna.json` | a quick view, no code |
| App page | Crow code in the repository (`app/scanner.co`) | the file | a real UI: inputs, actions, orders |

A dashboard made in Myna's pages is written into `myna.json` as it is
made; there is nothing to export. A tile's answer is cached under
`data/.tiles/`.

## Making a dashboard, in finchdash

Three ways, by who is making it.

**A view with no code**, by anyone with an editor's grant. On the Query
page, pick a table (`report_trades`), a verb (Newest run), the columns,
and Run; Save it as a named query (`P&L by symbol`); Pin it to a
dashboard, new or existing. On the Dashboards page, New dashboard names
one; Add tile picks a saved query and how to draw it (table, number,
bars; Kite's lines and candles later); tiles are moved and removed in
place; a refresh interval is set; a program and its parameters are
named, so Run runs it and then refreshes the tiles. Every step writes
`finchdash/myna.json`, and the Code page (or git) commits it.

**A table written by a notebook**, by someone exploring. A notebook
`notebooks/gate_study.co` reads the day's bars and writes
`data/gate_by_minute`; the Jobs page schedules it (its schedule in
`myna.json`); queries over the table are pinned as above. The notebook
is the dashboard's program; the file is its code.

**A page with inputs and actions**, by a developer. On the Code page or
in any editor, a file `app/orders.co` holds the page: its variables are the
inputs, its functions the actions, its `render` view draws them inside
`myna.screen[…]` (the example above). Two lines register it: in
`main.co`, `page['/orders', orders.render]`; in `myna.json`,
`{"name": "Orders", "page": "/orders"}` under `dashboards`, so the
sidebar lists it with the others. `crow run main.co`, or Compile, and the
page is there. Its tests are Crow's own, in the file (`app[render]`,
`click`, `change`, as finch's views are tested), and the commit is git's.

## What Myna keeps where

| | Was (rows in the data folder) | Is (2026-11-07) |
|---|---|---|
| Notebooks and their versions | `_notebooks` | `notebooks/<name>.co`; git for history |
| Saved queries | `_queries` | `queries/<name>.json` |
| Dashboards and tiles | `_dashboards`, `_tiles` | `myna.json` (`dashboards`, each tile's query inline) |
| Schedules | `_schedules` | `myna.json` (`jobs`) |
| Settings | `_settings` | `myna.json` (`settings`; the workspace's name in the scratch project's) |
| Runs (status, time, output) | `_runs` | `data/_runs` — data, unchanged |
| Experiments, models, traces | the data folder | unchanged — data |
| Tile answers | `_tiles`, `data/.tiles/` | `data/_answers` (keyed by dashboard and title) and `data/.tiles/` |
| The project registry | `myna_data/_projects` | unchanged — records |
| The scratch work (no project open) | `myna_data/` itself | `myna_data/scratch/`, a project like any other |

**A notebook is a Crow program.** `notebooks/<name>.co` is plain Crow
with cell marks, `--- %% <title>` lines, so the file runs with
`crow run`, diffs and reviews as code, and opens in any editor; Myna's
Code page shows it as cells, runs it as one program,
and writes the file on save. A save over a file changed since it was
opened is refused with what changed.

## The layers

- **Crow** is the language and the runtime: programs, live pages (a view
  drawn on the server, its inputs bound to variables, its handlers plain
  functions), and widgets drawn in the browser.
- **Packages** are what a project depends on: **Magpie** (the data store,
  every table a log), **Myna** (the platform: the shell every page shares,
  the data services, notebooks, queries, jobs, experiments, models) and
  **Lory** with **Kite** (graphics: 2D and 3D scenes, charts, games).
- **Projects** are what people build: finchdash depends on all of the
  above and holds its own pages and programs. Myna holds nothing of any
  project.

An app is built *on* Myna the way a web app is built on a framework:
Myna is a dependency of the project, never the other way round.

## How a dashboard is built when the code lives in the project

A dashboard is a Crow page in the project's repository. Its inputs are
variables, its actions are functions, its view draws them:

```
use web, ui, frame, magpie
use myna
use finch.scanner, finch.paper

min_price = 2.0
max_price = 20.0
symbol = ''
qty = 100

fn save_settings[]
    w = magpie.batch['data/scanner_settings', frame.new[min_price = [min_price], max_price = [max_price]], by = ['key']]

fn buy[]
    placed = paper.place[symbol, 'BUY', qty]      --- the project's paper book, a log

view render[]
    return myna.screen['VWAP Scanner', stack[
        row[field['Min Price', min_price], field['Max Price', max_price], button['Save', click = save_settings]],
        table[scanner.rows[min_price, max_price], sort = true],
        row[field['Symbol', symbol], field['Qty', qty], button['Buy', click = buy, class = 'primary']]
    ]]
```

The page, the project's modules and the Myna package compile together
into one program: the project's `main.co`, which registers Myna's
standard pages (Notebooks, Catalog, Query, Jobs, Experiments, Models)
beside the project's own and serves them. That program is **the
project's process**. Nothing of the project is loaded into Myna; Myna is
loaded into the project. The shell — the sidebar, the top bar, the theme —
comes from the package, so every project looks like Myna; the project's
`css/app.css` styles its own pages. Only what a project uses is compiled
in.

A handler runs on the server, in the project's process, so it can do
anything the project's modules can: write a log, place a paper order, run
a program, read the broker's paper API. The browser is a live view of the
page and holds no logic.

## Reaching a project

**Now.** An app project's process is run from its folder (`crow run
main.co`, or the binary Compile built) and serves on its own port. A
project without an app is served by Myna's own server, which lists the
projects, opens one and makes new ones. One person, one machine, their
own checkout.

**Later: the workspace server.** The same Myna server becomes the front
door of a workspace: sign-in, the users and their grants, the projects.
It starts an app project's process on the first visit and stops an idle
one, and forwards `/p/<project>/…` to that process — pages and their
sockets alike — after checking that the reader may see the project. The
process learns who is asking from a header the server adds, and listens
on a port only the server reaches. This needs two things in Crow's web
runtime that are not there yet: forwarding a route (HTTP and WebSocket)
to another server, and a base path, so a process serving under
`/p/finchdash/` writes its links and its socket path there. Nothing a
project builds now changes when this arrives: the unit is the process
either way.

## A workspace many people use at once

Several people work in the same workspace, on the same or different
projects, from their browsers, and none of them runs a server: one Myna
server per workspace, on a machine of its own, is the whole deployment.

- **A session is the reader's.** Each browser connection holds its own
  page state (Crow's live pages), and a signed cookie carries who is
  signed in (`sign_in`, `reader`). The project a reader is working in is
  their process's (below), never a pointer every reader shares.
- **A checkout per reader.** Code is edited in git's way: the server
  holds a bare repository per project and a checkout of it per reader
  (`users/<reader>/<project>/`). A reader's saves land in their checkout;
  Myna's Code page shows the changes and commits and pushes them; others
  pull. Two readers never write one file, and a conflict is git's to
  show. On one machine with one reader, their own checkout is all there
  is.
- **One data folder per project**, shared by every reader's checkout,
  under the workspace's data root. Magpie's design is one process writing
  a log, and the server is that process. A notebook's run, a program's
  run and an app project's process reach the logs through Myna's data
  route, which speaks Magpie's door protocol and checks the grant (Access
  to data, below): every verb given `http://…/data/<project>/<table>`
  answers as the directory would, so there is one store.
- **Users and grants** are logs of the workspace: `_users` (each with a
  workspace role, admin or member) and `_grants` (reader × project ×
  role: viewer, editor, owner). A page checks the reader's grant before
  it reads or writes a project. Passwords are hashed with Crow's
  `hash[…, 'password']` (Argon2id), and the sign-in is Crow's signed
  cookie (`sign_in`, `reader`).
- **A process per reader and project.** Crow hands a plain function no
  session fact — not the reader, not a module variable — and Myna's data
  layer is plain functions over one folder. So a process serves one
  project, fixed when it starts, and the workspace server starts one per
  reader and project (as JupyterHub starts a server per user) and
  forwards to it. The process runs in the reader's checkout, so a
  checkout per reader comes with it. On one machine, the one process is
  the reader's own.
- **Runs are processes.** A notebook or a program runs as a child process
  in the reader's checkout, under a time limit and, later, a memory limit
  and a queue, so one reader's heavy run stalls no page. Later still the
  scheduler hands runs to worker machines; the door makes the store
  reachable from them already.

What an exploration shares with an app: the project (a repository and a
data folder), Myna's pages, jobs and the scheduler, experiments and
models. What differs: no pages, no Compile and no process of its own; it
is served by the workspace server in process.

## Access to data

Every byte that is not code is in Magpie: a project's tables, its runs,
experiments, models and traces, and the workspace's own records of
projects, users and grants. What a reader may reach is the workspace's
decision, made the same way wherever the data is touched:

- **The workspace owns the data folders.** A project's data folder lies
  under the workspace's data root (`<root>/<project>/`), not in anyone's
  checkout; the manifest's `data/` is only the default for one person's
  own machine. A reader names a project, never a path, and the server
  resolves the folder and checks the grant.
- **Myna's pages check in process.** Catalog, Query, Notebooks, Jobs,
  Experiments and Models read and write a project's logs only after the
  reader's grant on that project allows the verb: a viewer reads, an
  editor writes, an owner grants.
- **Processes check through the server.** A notebook's run, a program's
  run and an app project's process hold no path to the logs: they are
  given a URL and a token for the run, and reach the data by Magpie's
  door protocol at a route of Myna's (`/data/<project>/<table>/<verb>`),
  which checks the token's grants and then calls the Magpie verb on the
  directory. Magpie stays a store: its one addition is a hook on the
  door, `door[root, port, allow = fn]`, a function asked per request
  with the token, the log and the verb, so Myna's check is the door's own
  and no second server is needed. A run writing a project it may only
  read is refused.
- **On one machine with one reader**, the owner holds every grant, and
  the same code runs with the check always passing.

## Editing code

The code is edited in Myna's Code page (`/`, built 2026-11-07) or in
any editor: the page is the file tree, the cells or the text of a file,
the Run, Test and Check console, and the Git drawer over the reader's
checkout. The cell or file being edited is drawn by Lory in WebGL: the
editor began as Lory Studio (`lory/studio/`, 2026-11-07), a separate
server over a project's folder, and moved into Myna as `drawn/editor.co`
and `drawn/edit.co` when the page took it; Studio is retired, since Lory
is the graphics package, not an application. A project's notebooks run
in the project's folder, so a cell can `use finch.scanner`, read the
project's files and run its programs.

How the editor is built: the Code page is a page of the workbench, so
the screen's sign-in and grant checks cover it, and the cell or file
being edited is `widget['editor', props = map[text = …, mode = …], on =
map[change = …, save = …, run = …, whole = …]]`. Its module,
`widgets/editor.js`, mounts the editor program (`drawn/edit.co`, built
for the web into `drawn/edit_web/` and served at `/edit/` — `web/` links
it beside the drawn workbench) in the widget's element, gives it the
text as props, and sends what the editor asks — the text as it is now,
Ctrl+S, Ctrl+Enter, Ctrl+Shift+Enter — as the widget's events, which
the page's handlers take as they take a field's text, so a save checks
the reader's grant as every writing handler does. No route and no token
were needed: the design had the editor reach the files through
`/code/api/…` routes with a token signed for the reader, which stays the
way for a client that is not the page itself. One editor is drawn at a
time (one WebGL context), and its context is kept between the cells
edited; the cells not being edited are text the page renders.

## Myna's pages, each project's own

When a project is selected, every page of Myna reads that project: its
notebooks and queries from the repository, its catalog, runs, jobs,
experiments, models and traces from the data folder. The project's
programs are jobs too: the Jobs page runs them, schedules them (the
schedule in `myna.json`) and keeps their output. The sidebar's top names
the workspace and switches projects; the workspace's own pages (Projects;
later Users and Access) sit beside them.

## Graphics

A page draws a chart or a scene with a widget: the server owns the data
and hands it to the widget as props; Lory or Kite draws it in the browser
and redraws when the props change. Myna's drawn workbench (`drawn/`) is
built this way, and a project's pages use the same packages the same
way. Kite's charts (lines, candles) replace Myna's own bar and number
tiles once Kite is complete.

## What is built and what is not

Built: projects as folders with a manifest, a data folder and compiled
programs; the project registry; tile dashboards (kept as rows still);
Run and Compile; every Myna page reading the open project; the project
format (finchdash/docs/project-format.md). The admin section (2026-11-07): users
and their roles, grants per project, sign-in with Crow's cookie, the
Users and Access pages, every page asking for a sign-in once the
workspace has users and showing a reader with no grant that they have
none, and the writing handlers refusing a reader without an editor's
grant (an admin needs none; a workspace with no users is one reader's,
an admin's).

Code as files (2026-11-07): notebooks, queries, dashboards, schedules
and settings are the project's files, as the table above says; New
project runs `git init`; a notebook's History lists its commits and
restores one; the scratch project is a project like any other.

The Code page (2026-11-07) absorbs the Notebooks page: the project's
files in a tree, the notebooks first, each opened as a tab; a `.co` file
as cells or as text, any other file as text; a file run, tested or
type-checked whole with the output in a console under the editor; a git
drawer with the branch, the changes, Init, Commit, Pull and Push; and
History listing a file's runs and commits. Its editor (2026-11-07) is
Lory's, drawn in WebGL in the cell or file being edited: line numbers,
Crow coloured, Tab and Shift+Tab, Enter keeping the indent, the wheel
scrolling by the pixel, Ctrl+S to save, Ctrl+Enter to run, a paste as
typed text (Editing code, above); Lory Studio's page and server are
retired.

Myna as a package (2026-11-07): the package is the folder `myna/` — the
modules, `css/`, `widgets/`, `web/` (links to the web builds) and the
scheduler — which an app names in its crowfile (`myna = '../myna/myna'`,
a release later) and imports with `use myna`. The app's `main.co` is
`myna.ready[port]` (its own folder opened as the project, the workspace
ready, the styles and widgets linked beside it, the port noted for the
scheduler), its own `serve[…, files = myna.builds[]]` — a server starts
only from a program's top level, so the line is the app's — and
`myna.pages[]`, then its own pages. A dashboard of the manifest with a
`page` is listed in the sidebar after Myna's sections, and its tab on the
Dashboards page opens the page. Myna's own `main.co` is the same three
lines. finchdash is the first app: `app/scanner.co` is finch's VWAP
Scanner page over the recorded day, with its inputs, its tables and its
order bar to the paper book.

An app's own widgets and web builds (2026-11-10): the page's shell reads
`widgets/*.js` from the program's folder and the server hands out one
folder of files, so an app that draws something of its own — finchdash's
charts, a Crow program drawn by Lory and Kite and built for the web —
keeps both folders itself. With a `widgets/` folder of its own modules,
`myna.ready` links each of Myna's widgets into it (the Code page's editor
beside the app's chart); with a `web/` folder holding a link to its
build, `myna.builds` links Myna's builds into it (`/edit/`, `/drawn/`
beside the app's `/charts/`) and answers `web` as the server's files.
Myna's own folders are linked whole where the app has neither, as before.

Not built, in the order to build it:

1. The rest of the admin section: the data route, and Magpie's `allow`
   hook on the door (waiting on a Magpie change under way).
2. finchdash's other pages (simulation, jobs, telemetry, execution,
   budgets, reports); Myna as a released package (a tag, the web builds
   shipped with it).
3. Programs as scheduled jobs; the project switcher in the sidebar.
4. Runs reaching the store through the door; a process and a checkout
   per reader; the workspace server and its forwarding; several data
   folders per project.
5. The editor's selection, search and a monospaced face (Lory's atlas
   draws one font); the cells not being edited coloured as the editor
   colours them.
